from function_mqtt import *

client.on_message = on_message
client.connect("31.186.100.61", 1883, 60)

subscribe_device("1")

client.loop_forever()
