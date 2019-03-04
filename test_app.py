
import os

from flask import jsonify
import pytest

from myapp import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_authen(client):
    rv = client.post('/device/authen', json={
        'id': 1, 'passwd': 'ljhandlwt'
    })
    json_data = rv.get_json()
    assert json_data['msg'] == 'ok'


def test_statistics(client):
    rv = client.post('/statistics', json={'id':'all'})
    json_data = rv.get_json()
    assert json_data.get('liveDevices', None) is not None


def test_deviceInfo(client):
    rv = client.post('/device')
    json_data = rv.get_json()
    assert len(json_data) > 0
    