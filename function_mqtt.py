import paho.mqtt.client as mqtt
import json

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="algalar_the_best", password="1Qaz2Wsx")

i = 0


def on_message(client, userdata, message):
    topic_lst = message.topic.split('/')
    text = message.payload.decode('utf-8')
    # print(message.topic, message.payload.decode('utf-8'))

    if topic_lst[1] == "state_number":
        state_number(topic_lst, text)
    if is_device_reg(topic_lst):
        if topic_lst[1] == "quest":
            if text == "get wheels":
                push_wheel_data(int(topic_lst[0]))
            if "wheel_" in text:
                push_all_wheel_data(int(topic_lst[0]), text)
        if topic_lst[1] == "wheel":
            pass


def state_number(topic: list, state_number: str):
    with open('save_mqtt_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open('Cars.json', 'r', encoding='utf-8') as file:
        cars = json.load(file)

    for car in cars:
        print(car["id"])
        if state_number == car['gosnum']:
            data[str(topic[0])] = car["id"]
            break

    with open('save_mqtt_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    print(f"{topic[0]}/answer", "OK")
    client.publish(f"{topic[0]}/answer", "OK")


def push_wheel_data(id_device: int):
    with open('save_mqtt_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    car_id = data[str(id_device)]

    with open('Wheels.json', 'r', encoding='utf-8') as file:
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

    with open('Wheels.json', 'r', encoding='utf-8') as file:
        wheels = json.load(file)

    lst = ""

    for wheel in wheels:
        if wheel["id_car"] == car_id:
            for i in wheel[wheel_id]:
                lst += str(wheel[wheel_id][i]) + " "
            break
    print(f"{id_device}/answer", lst)
    client.publish(f"{id_device}/answer", lst)

def subscribe_device(device_id):
    client.subscribe(f"{device_id}/#")
