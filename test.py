# import paho.mqtt.client as mqtt
#
#
#
# # Создаем клиент MQTT
# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.username_pw_set(username="algalar_the_best", password="1Qaz2Wsx")
#
# # Подключаемся к брокеру
# client.connect("31.186.100.61", 1883, 60)
#
# # Отправляем сообщение в топик
# # client.publish(f"1/state_number", "А121АА196")
# client.publish(f"1/quest", "get wheels")
# # client.publish("1/quest", "wheel_3")
# # client.publish("1/quest", "get wheels")
# # client.publish("1/quest", "get wheels")
#
# # Отключаемся от брокера
# client.disconnect()
from datetime import datetime, timedelta


def round_to_seconds(dt):
    return dt.replace(microsecond=0)


# Функция для определения количества секунд в каждом интервале относительно текущего времени
def calculate_seconds_intervals(seconds_list):
    current_time = round_to_seconds(datetime.now())
    first_time = current_time - timedelta(seconds=seconds_list[-1])

    intervals = []
    for seconds in seconds_list:
        interval_time = first_time + timedelta(seconds=seconds)
        intervals.append(str(interval_time))

    return intervals


# Пример списка секунд
seconds_list = list(range(120))

# Получение интервалов времени относительно текущего времени
intervals = calculate_seconds_intervals(seconds_list)

# Вывод результатов
for i, interval in enumerate(intervals):
    print(seconds_list[i], "\t", interval)
