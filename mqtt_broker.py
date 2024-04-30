from function_mqtt import *

client.on_message = on_message
client.connect("31.186.100.61", 1883, 60)
subscribe_device("1")
subscribe_device("2")
subscribe_device("3")
subscribe_device("4")
subscribe_device("5")
subscribe_device("45")
while 1:
    try:
        client.loop_forever()
    except Exception as e:
        pass
