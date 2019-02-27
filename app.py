
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def create_app(test_config=None, debug=True, testing=False):
    # create and configure the app
    app = Flask(__name__)

    if debug:
        app.config.from_object('config.DebugConfig')
    elif testing:
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.ProductionConfig')
    db.init_app(app)
    
    # @app.route('/')
    # def index():
        # return 'hello'
    
    import views
    app.register_blueprint(views.bp)
    
    from subscriber import client
    client.on_message = on_message
    client.loop_start()
    
    return app

app = create_app()


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
