from function_mqtt import *

client.on_message = on_message
client.connect("5.188.138.91", 1883, 60)
subscribe_device("1")
subscribe_device("2")
subscribe_device("3")
subscribe_device("4")
subscribe_device("5")
subscribe_device("6")
subscribe_device("7")
subscribe_device("8")
subscribe_device("9")
subscribe_device("10")
subscribe_device("100")
while 1:
    try:
        client.loop_forever()
    except Exception as e:
        pass

