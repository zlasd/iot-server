import base64
import time
import json
from sys import argv

import paho.mqtt.client as mqtt

from config import Config


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Published message #" + str(mid))

client = mqtt.Client("publisher")
client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set(Config.MQTT_USER,
            password=Config.MQTT_PASSWD)

client.connect("127.0.0.1", 1883, 60)
print("connected")

# img_gif = 'Negev_lily.gif'
img_jpg = 'test1.jpg'


ENCODING = 'utf-8'    # 指定编码形式
IMAGE_NAME = "env/" + img_jpg

# 读取二进制图片，获得原始字节码，注意 'rb'
with open(IMAGE_NAME, 'rb') as jpg_file:
    byte_content = jpg_file.read()

# 把原始字节码编码成 base64 字节码
base64_bytes = base64.b64encode(byte_content)

# 将 base64 字节码解码成 utf-8 格式的字符串
base64_string = base64_bytes.decode(ENCODING)

# 用字典的形式保存
raw_data = {}
raw_data["serial-number"] = "设备1"
raw_data["passwd"] = "ljhandlwt"
raw_data["image_base64_string"] = base64_string
raw_data["personNo"] = 2
raw_data["confidence"] = 1

# 将字典变成 json 格式，缩进为 2 个空格
json_data = json.dumps(raw_data, indent=2)
#print(type(json_data))
#client.loop()
#base64_data = base64.b64encode(f.read())
client.publish("/device/alert", json_data, 1)
time.sleep(1)
client.disconnect()