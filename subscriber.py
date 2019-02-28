
import time

import paho.mqtt.client as mqtt

BROKER_IP = "127.0.0.1"
TOPIC = "/device/#"

import config


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

client.subscribe(TOPIC, 1)
print('subscribe the topic ', TOPIC,' succuessfully')

client.on_log = on_log
client.on_message = on_message
client.loop_forever()