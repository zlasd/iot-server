import paho.mqtt.client as mqtt
import base64
import json

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import config
from models import Base, Device, Alert



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(("hello/world", 1))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #get the alert info
    img_jpg = 'test1_1.jpg'
    json_data=msg.payload
    raw_data=json.loads(str(json_data, encoding="utf-8"))
    base64_string = raw_data["image_base64_string"]
    img_data = base64.b64decode(base64_string)
    imgfile = open("/home/zhanghua/Downloads/" + img_jpg, 'wb')
    imgfile.write(img_data)
    imgfile.close()

    app = Flask(__name__)
    app.config.from_object('config')

    engine = create_engine(app.config['DB_CONNECT_STRING'], echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    #Base.metadata.create_all(engine)
    device = Device(name='camera0',type=raw_data["type"],addr=raw_data["address"],passwd=raw_data["passwd"])
    alert=Alert(deviceID=device.ID,personNo=raw_data["personNo"],confidence=raw_data["confidence"])
    session.add(device)
    session.add(alert)
    session.commit()
    session.close()




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
