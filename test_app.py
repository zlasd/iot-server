
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
    rv = client.get('/authen?id=200&passwd=崩崩崩')
    
    with app.app_context():
        resp = rv.get_json()
        ground_truth = jsonify({"id":"200", "passwd":"崩崩崩"}).get_json()
        assert resp == ground_truth

