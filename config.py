import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = b'\xe5\xfd\xc9\x8c1\xf5\x9f\x953\xbe\x83.\x92\x0eC\xf4'
    
    MAIN_TITLE = 'WebServer'
    PORT = 8080
    
    DATABASE_NAME = 'WebServer'
    DATABASE_USERNAME = 'root'
    DATABASE_PASSWORD = 'passw0rd'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1/{}' \
        .format(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MQTT_USER = 'localmqtt'
    MQTT_PASSWD = '123456'
    MQTT_IMG_PATH = 'env/alert-img/'
    


class DebugConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True