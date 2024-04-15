import paho.mqtt.client as mqtt



# Создаем клиент MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="algalar_the_best", password="1Qaz2Wsx")

# Подключаемся к брокеру
client.connect("31.186.100.61", 1883, 60)

# Отправляем сообщение в топик
# client.publish(f"1/state_number", "А121АА196")
client.publish(f"1/quest", "get wheels")
# client.publish("1/quest", "wheel_3")
# client.publish("1/quest", "get wheels")
# client.publish("1/quest", "get wheels")

# Отключаемся от брокера
client.disconnect()