import functools

from flask import (
    Blueprint, jsonify, request
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('view', __name__)


@bp.route('/authen')
def authen():
    id = request.args.get('id', 'null')
    passwd = request.args.get('passwd', 'null')
    return jsonify({"id":id, "passwd":passwd})


@bp.route('/statistics/<devices>')
def getStatistics(devices):
    devices = devices.split('-')
    return jsonify(devices)

