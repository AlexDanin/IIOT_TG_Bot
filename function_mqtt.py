import paho.mqtt.client as mqtt
import json
from datetime import datetime, timedelta

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="algalar_the_best", password="1Qaz2Wsx")

i = 0


def round_to_seconds(dt):
    return dt.replace(microsecond=0)


# Функция для определения количества секунд в каждом интервале относительно текущего времени
def calculate_seconds_intervals(seconds_list):
    current_time = round_to_seconds(datetime.now())
    first_time = current_time - timedelta(seconds=int(seconds_list[-1]))

    intervals = []
    for seconds in seconds_list:
        interval_time = first_time + timedelta(seconds=int(seconds))
        intervals.append(str(interval_time))
    print(intervals)
    return intervals


def on_message(client, userdata, message):
    topic_lst = message.topic.split('/')
    text = message.payload.decode('utf-8')
    print(message.topic, message.payload.decode('utf-8'))

    if topic_lst[1] == "state_number":
        state_number(topic_lst, text)
    if is_device_reg(topic_lst):
        if topic_lst[1] == "quest":
            if text == "get wheels":
                push_wheel_data(int(topic_lst[0]))
            if "wheel_" in text:
                push_all_wheel_data(int(topic_lst[0]), text)
        if topic_lst[1] == "temp" or topic_lst[1] == "pres" or topic_lst[1] == "time":
            add_sensor_data(topic_lst[1], text, topic_lst[0], topic_lst[2])
        # if topic_lst[1] == "pres":
        #     add_sensor_data("pres", text, topic_lst[0], topic_lst[2])


def add_sensor_data(name: str, value: str, device_id: str, sensor_id: str):
    with open('data/Sensors_Data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(value.split('\r\n')[:-1])

    if name == "time":
        lst = calculate_seconds_intervals(value.split('\r\n')[:-1])
    else:
        lst = value.split('\r\n')[:-1]

    # if len(data) != 0:
    if device_id in data.keys():
        if sensor_id in data[device_id].keys():
            if name in data[device_id][sensor_id].keys():
                data[device_id][sensor_id][name].extend(lst)
            else:
                data[device_id][sensor_id][name] = lst
        else:
            data[device_id][sensor_id] = {}
            data[device_id][sensor_id][name] = lst
    else:
        data[device_id] = {}
        data[device_id][sensor_id] = {}
        data[device_id][sensor_id][name] = lst

    with open('data/Sensors_Data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    print("wtf")


def state_number(topic: list, state_num: str):
    with open('save_mqtt_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    with open('data/Cars.json', 'r', encoding='utf-8') as file:
        cars = json.load(file)
    flag = False
    for car in cars:
        # print(car["id"])
        # print(state_num, car['gosnum'])
        # print(state_num == car['gosnum'])
        if state_num == car['gosnum']:
            flag = True
            print(state_num, car['gosnum'])
            data[str(topic[0])] = car["id"]
            break
    if not flag:
        print(f"{topic[0]}/answer", "not")
        client.publish(f"{topic[0]}/answer", "not")
        return
    with open('save_mqtt_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)
    wheel_count = 0
    for wheel in wheels:
        if wheel["id_car"] == data[str(topic[0])]:
            for i in wheel:
                if "wheel_" in i:
                    wheel_count += 1
    print(f"{topic[0]}/answer", str(wheel_count))
    client.publish(f"{topic[0]}/answer", str(wheel_count))


def push_wheel_data(id_device: int):
    with open('save_mqtt_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    car_id = data[str(id_device)]

    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    lst = ""

    for wheel in wheels:
        if wheel["id_car"] == car_id:
            for i in wheel:
                if "wheel_" in i:
                    lst += str(i[6:]) + " "
            break
    print(f"{id_device}/answer", lst)
    client.publish(f"{id_device}/answer", lst)


def is_device_reg(topic: list):
    with open('save_mqtt_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    return str(topic[0]) in list(data.keys())


def push_all_wheel_data(id_device: int, wheel_id: str):
    with open('save_mqtt_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    car_id = data[str(id_device)]

    with open('data/Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    lst = ""

    try:
        for wheel in wheels:
            if wheel["id_car"] == car_id:
                for i in wheel[wheel_id]:
                    lst += str(wheel[wheel_id][i]) + " "
                break
        print(f"{id_device}/answer", lst)
        client.publish(f"{id_device}/answer", lst)
    except Exception as e:
        print(e)


def subscribe_device(device_id):
    client.subscribe(f"{device_id}/#")
