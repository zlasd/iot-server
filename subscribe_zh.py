import os
import datetime
import base64
import json
import traceback
from functools import wraps

import requests
import paho.mqtt.client as mqtt


from myapp import app, db
from models import Device, Alert


def error_prone(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            f(*args, **kwds)
        except Exception as ex:
            print(traceback.format_exc())
    return wrapper

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


@error_prone
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
    
    
@error_prone
def alert(client, userdata, msg):
    # unpack json payload
    json_data=msg.payload
    raw_data=json.loads(str(json_data, encoding="utf-8"))
    
    with app.app_context():
        device = Device.query.filter_by(
            name=raw_data["serial-number"]).first()
        alert=Alert(deviceID=device.ID,
            personNo=raw_data["personNo"],
            confidence=raw_data["confidence"])
        db.session.add(alert)
        db.session.commit()
        
        deviceID = device.ID
        alertID = alert.alertID
        personNo = alert.personNo
        confidence = alert.confidence
        time = alert.time
       
    #save alert image
    os.makedirs(app.config['MQTT_IMG_PATH'], exist_ok=True)
    img_path = app.config['MQTT_IMG_PATH'] + 'alert-' + str(alertID) + '.gif'
    base64_string = raw_data["image_base64_string"]
    img_data = base64.b64decode(base64_string)
    with open(img_path, 'wb') as imgf:
        imgf.write(img_data)

    # notify HTTP server in localhost
    payload = {
        'deviceID': deviceID, 
        'alertID': alertID,
        'time': time,
        # 'alertInfo':{
            # 'personNo': personNo,
            # 'confidence':confidence,
        # }
    }
    print(payload)
    requests.post("http://127.0.0.1:"+str(app.config['PORT'])+"/device/alert",
        headers={"Content-Type": "application/json"}, data=payload)

        
def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '"
          + msg.topic + "' with QoS " + str(msg.qos))


client = mqtt.Client("subscriber")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(app.config["MQTT_USER"],
            password=app.config["MQTT_PASSWD"])

client.connect("0.0.0.0", 1883, 60)


client.subscribe('/device/#', 1)
client.message_callback_add('/device/add', deviceAdd)
client.message_callback_add('/device/alert', alert)
print("add callback")

client.loop_forever()
