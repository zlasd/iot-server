import paho.mqtt.client as mqtt
import base64
import json
from flask import jsonify
from sys import argv

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '"
          + msg.topic + "' with QoS " + str(msg.qos))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("hachina", password="123456")
client.connect("127.0.0.1", 1883, 60)


img_gif = 'Negev_lily.gif'
img_jpg = 'test1.jpg'
ENCODING = 'utf-8'   #指定编码格式
IMAGE_NAME = "/home/zhanghua/Downloads/" + img_jpg

# 读取二进制图片，获得原始字节码，注意 'rb'
with open(IMAGE_NAME, 'rb') as jpg_file:
    byte_content = jpg_file.read()

# 把原始字节码编码成 base64 字节码
base64_bytes = base64.b64encode(byte_content)

# 将 base64 字节码解码成 utf-8 格式的字符串
base64_string = base64_bytes.decode(ENCODING)

# 用字典的形式保存数据
raw_data = {}
raw_data["name"] = IMAGE_NAME
raw_data["image_base64_string"] = base64_string

# 将字典变成 json 格式，缩进为 2 个空格
json_data = json.dumps(raw_data, indent=2)
print(type(json_data))

#base64_data = base64.b64encode(f.read())
client.publish("hello/world", json_data)