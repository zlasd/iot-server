
import time

import paho.mqtt.client as mqtt

BROKER_IP = "127.0.0.1"

import config


def on_log(client, userdata, level, buf):
    print("log: ",buf)


client = mqtt.Client("Subscriber")
print('Client created')

client.connect(BROKER_IP)
print('connect to broker')

client.subscribe("/demo", 1)
print('subscribe the topic /demo succuessfully')

client.on_log = on_log
