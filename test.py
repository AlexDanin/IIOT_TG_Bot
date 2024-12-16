import paho.mqtt.client as mqtt

# Создаем клиент MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="algalar_the_best", password="1Qaz2Wsx")

# Подключаемся к брокеру
client.connect("5.188.138.91", 1883, 60)

# Отправляем сообщение в топик
client.publish(f"device1/state_number", "8HPH19")
# client.publish(f"device2/topic2", "uuu")
# client.publish(f"100/quest", "get wheels")
# client.publish("100/quest", "wheel_3")
# client.publish("100/quest", "get wheels")
# client.publish("100/quest", "get wheels")

# Отключаемся от брокера
client.disconnect()


# from datetime import datetime, timedelta
#
#
# def round_to_seconds(dt):
#     return dt.replace(microsecond=0)
#
#
# # Функция для определения количества секунд в каждом интервале относительно текущего времени
# def calculate_seconds_intervals(seconds_list):
#     current_time = round_to_seconds(datetime.now())
#     first_time = current_time - timedelta(seconds=seconds_list[-1])
#
#     intervals = []
#     for seconds in seconds_list:
#         interval_time = first_time + timedelta(seconds=seconds)
#         intervals.append(str(interval_time))
#
#     return intervals
#
#
# # Пример списка секунд
# seconds_list = list(range(120))
#
# # Получение интервалов времени относительно текущего времени
# intervals = calculate_seconds_intervals(seconds_list)
#
# # Вывод результатов
# for i, interval in enumerate(intervals):
#     print(seconds_list[i], "\t", interval)


# import matplotlib.pyplot as plt
#
# # Пример данных
# x = [1, 2, 3, 4, 5]
# y1 = [3, 5, 2, 7, 4]
# y2 = [4, 6, 3, 8, 5]
#
# # Создание точечного графика с двумя наборами данных
# plt.scatter(x, y1, color='blue', marker='o', label='Группа 1', facecolor="black")  # Группа 1
# plt.scatter(x, y2, color='red', marker='x', label='Группа 2', facecolor="black")   # Группа 2
#
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Пример точечного графика с легендой')
#
# # Добавление легенды
# plt.legend()
#
# plt.grid(True)
# plt.show()


