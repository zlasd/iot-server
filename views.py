import functools
from datetime import datetime, timedelta

from flask import (
    Blueprint, jsonify, request
)
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
import requests


bp = Blueprint('view', __name__)


from models import Device, Alert


@bp.route('/device/authen', methods=['POST'])
def authen():
    id = request.json.get('id', 1)
    if type(id) != int:
        id = int(id)
    passwd = request.json.get('passwd', "")
    
    try:
        dev = Device.query.filter_by(ID=id).first()
        ok = check_password_hash(dev.passwd, passwd)
        msg = "password not correct." if not ok else "ok"
    except Exception as ex:
        ok = False
        msg = "Parameters broken"
    return jsonify({"result":ok, "msg":msg})


@bp.route('/device', methods=['GET', 'POST'])
def deviceInfo():
    devices = Device.query.filter_by(live=True).all()
    collect = []
    for dev in devices:
        collect.append({
            "deviceID": dev.ID,
            "name": dev.name,
            "type": dev.type,
            "address": dev.address,
            "joinTime": dev.joinTime
        })
    return jsonify(collect)


@bp.route('/statistics', methods=['POST'])
def getStatistics():
    # get params
    devicesID = request.json.get('id', 'all')
    
    # query database
    now = datetime.now()
    devices = Device.query.filter_by(live=True)
    alerts = Alert.query
    devices_weekly = Device.query
    alerts_weekly = Alert.query
    
    
    try:
        # if IDs are given, filtering
        if devicesID != 'all':
            devices = devices.filter(Device.ID.in_(devicesID))
            alerts = alerts.filter(Alert.deviceID.in_(devicesID))
            devices_weekly = devices_weekly.filter(
                Device.ID.in_(devicesID))
            alerts_weekly = alerts_weekly.filter(
                Alert.deviceID.in_(devicesID))    
        
        # apply query
        devices = devices.all()
        alerts = alerts.all()
        devices_weekly = devices_weekly.filter(
            Device.joinTime.between(now-timedelta(days=7), now)
        ).count()
        alerts_weekly = alerts_weekly.filter(
            Alert.time.between(now-timedelta(days=7), now)
        ).count()
    except Exception as ex:
        return jsonify({"msg":"Parameters broken, check params type"})
    
    # response framework
    collect = {
        "liveDevices": len(devices),
        "newDevicesWeekly": devices_weekly,
        "totalAlert": len(alerts),
        "alertWeekly": alerts_weekly,
        "deviceList": [],
        "alertList": [],
    }
    
    for dev in devices:
        collect['deviceList'].append({
            "deviceID": dev.ID,
            "name": dev.name,
            "type": dev.type,
            "address": dev.address,
            "joinTime": dev.joinTime
        })
    for alert in alerts:
        collect['alertList'].append({
            "deviceID": alert.deviceID,
            "alertID": alert.alertID,
            "time": alert.time,
            "personNo": alert.personNo,
            "confidence": alert.confidence
        })
    
    return jsonify(collect)

    
@bp.route('/device/alert', methods=['POST'])
def alert():
    params = request.json
    deviceID = params.get('deviceID', None)
    if not deviceID:
        return jsonify({"result":False, "msg":"need device ID"})
    
    wx_url = 'http://'+app.config['WX_SERVER']+'/wechatserver/alert'
    alertID = params.get('alertID', None)
    if alertID is None:
        return jsonify({"result":False, "msg":"need alert ID"})
    time = params.get('time', None)
    time = datetime.now() if time is None else time
    
    img_url = 'http://{}:{}/static/alert-{}.gif'.format(app.config['MQTT_SERVER'], 8000, alertID)
    payload = {
        'alertid': alertID, 
        'deviceid': deviceID,
        'time': time,
        'imgurl': [img_url],
    }
    try:
        requests.post(wx_url, headers={"Content-Type":
            "application/json"}, data=payload)
    except Exception as ex:
        return jsonify({"result":False, "msg":"WX server error."})
    return jsonify({"result":True, "msg":"ok"})
    
    
@bp.route('/device/add', methods=['POST'])
def addDevice():
    name = request.form['name']
    type = request.form['type']
    addr = request.form['address']
    passwd = generate_password_hash(request.form['passwd'])
    new_device = Device(name, type, addr, passwd)
    from myapp import db
    db.session.add(new_device)
    db.session.commit()
    return jsonify({"name":name, "type":type,
            "addr":addr, "passwd":passwd})


@bp.route('/alert/add', methods=['POST'])
def addAlert():
    deviceID = request.form['deviceID']
    personNo = request.form['personNo']
    confidence = request.form['confidence']
    new_alert = Alert(deviceID, personNo, confidence)
    from myapp import db
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({"deviceID":deviceID,
            "personNo":personNo, "confidence":confidence})

