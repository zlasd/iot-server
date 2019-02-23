import os


CSRF_ENABLED=True
SECRET_KEY='ecgroup'

DATABASE_NAME = 'WebServer'
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = 'passw0rd'
DB_CONNECT_STRING = 'mysql+pymysql://{}:{}@127.0.0.1/{}' \
        .format(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME)

MAIN_TITLE = 'WebServer'