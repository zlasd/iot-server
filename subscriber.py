
import time

import paho.mqtt.client as mqtt

BROKER_IP = "127.0.0.1"

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


def on_log(client, userdata, level, buf):
    print("log: ",buf)


client = mqtt.Client("Subscriber")
print('Client created')

client.connect(BROKER_IP)
print('connect to broker')

client.subscribe("/demo", 1)
print('subscribe the topic /demo succuessfully')

client.on_message = on_message
client.on_log = on_log
client.loop_forever()