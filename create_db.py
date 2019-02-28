
from flask import Flask

from sqlalchemy_utils import database_exists, create_database

from myapp import app
from models import db

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

db.create_all(app=app)