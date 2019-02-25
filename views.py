import functools

from flask import (
    Blueprint, jsonify, request
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('view', __name__)


from models import Device, Alert


@bp.route('/authen')
def authen():
    id = request.args.get('id', 'null')
    passwd = request.args.get('passwd', 'null')
    return jsonify({"id":id, "passwd":passwd})


@bp.route('/statistics/<devices>')
def getStatistics(devices):
    devices = devices.split('-')
    return jsonify(devices)

    
@bp.route('/device/add', methods=['POST'])
def addDevice():
    name = request.form['name']
    type = request.form['type']
    addr = request.form['address']
    passwd = generate_password_hash(request.form['passwd'])
    new_device = Device(name, type, addr, passwd)
    from app import db
    db.session.add(new_device)
    db.session.commit()
    return jsonify({"name":name, "type":type,
            "addr":addr, "passwd":passwd})


@bp.route('/device/add', methods=['POST'])
def addAlert():
    deviceID = request.form['deviceID']
    personNo = request.form['personNo']
    confidence = request.form['confidence']
    new_alert = Alert(deviceID, personNo, confidence)
    from app import db
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({"deviceID":deviceID,
            "personNo":personNo, "confidence":confidence})

