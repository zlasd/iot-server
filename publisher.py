
import paho.mqtt.client as mqtt

BROKER_IP = "127.0.0.1"
TOPIC = "/device/alert"

def on_log(client, userdata, level, buf):
    print("log: ",buf)

client = mqtt.Client("Publisher")
print('Client created')

client.connect(BROKER_IP)
print('connect to broker')

client.on_log = on_log

# client.publish(TOPIC, 'app-to-app message', 0)
# print('publish to topic ', TOPIC)