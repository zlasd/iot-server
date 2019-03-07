import paho.mqtt.client as mqtt
import base64
import json
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(("hello/world", 1))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    img_jpg = 'test1_1.jpg'
    # 解码
    #img_data = base64.b64decode(msg.payload)
    json_data=msg.payload
    print(type(json_data))
    raw_data=json.loads(str(json_data))
    print(raw_data)
    base64_string = raw_data["image_base64_string"]
    img_data = base64.b64decode(base64_string)
    # 解码存储为动图
    imgfile = open("/home/zhanghua/Downloads/" + img_jpg, 'wb')
    imgfile.write(img_data)
    imgfile.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("hachina", password="123456")

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()