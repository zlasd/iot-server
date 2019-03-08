import datetime
import base64
import json

import requests
import paho.mqtt.client as mqtt


from myapp import app, db
from models import Device, Alert


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe((app.config['MQTT_TOPIC'], 1))
    message_callback_add('/device/add', deviceAdd)
    message_callback_add('/device/alert', alert)

def deviceAdd(client, userdata, msg):
    # unpack json payload
    json_data=msg.payload
    raw_data=json.loads(str(json_data, encoding="utf-8"))

    device = Device(raw_data["serial-number"],
        raw_data["type"], raw_data["addresss"],
        raw_data["passwd"])
    db.session.add(device)
    db.session.commit()
    print(datetime.datetime.now(), 
        "new device added:", raw_data["serial-number"])
    
    
def alert(client, userdata, msg):
    # unpack json payload
    json_data=msg.payload
    raw_data=json.loads(str(json_data, encoding="utf-8"))
    
    device = Device.query.filter_by(
        name=raw_data["serial-number"]).first()
    alert=Alert(deviceID=device.ID,
        personNo=raw_data["personNo"],
        confidence=raw_data["confidence"])
    db.session.add(alert)
    db.session.commit()
       
    #save alert image
    img_path = app.config['MQTT_IMG_PATH'] + 'alert-' + alert.alertID + '.jpg'
    base64_string = raw_data["image_base64_string"]
    img_data = base64.b64decode(base64_string)
    with open(img_path, 'wb') as imgf:
        imgf.write(img_data)

    # notify HTTP server in localhost
    payload = {'deviceID': device.ID, 
        'alertInfo':{
            'personNo': alert.personNo,
            'confidence':alert.confidence,
            'time': alert.time
        }
    }
    requests.post("http://127.0.0.1:"+app.config['PORT']+"/device/alert",
        headers={"Content-Type: application/json"}, data=payload)

        
def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '"
          + msg.topic + "' with QoS " + str(msg.qos))


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
