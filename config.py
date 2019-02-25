import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = b'\xe5\xfd\xc9\x8c1\xf5\x9f\x953\xbe\x83.\x92\x0eC\xf4'

    DATABASE_NAME = 'WebServer'
    DATABASE_USERNAME = 'root'
    DATABASE_PASSWORD = 'passw0rd'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1/{}' \
        .format(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIN_TITLE = 'WebServer'
    SERVER_NAME = '127.0.0.1:8080'

class ProductionConfig(Config):
    SERVER_NAME = '0.0.0.0:8080'

class DebugConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True