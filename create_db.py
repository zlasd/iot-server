
from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


import config
from models import Base, Device, Alert


app = Flask(__name__)
app.config.from_object('config')


engine = create_engine(app.config['DB_CONNECT_STRING'], echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
Base.metadata.create_all(engine)