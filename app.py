from datetime import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

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
    
    @app.route('/')
    def index():
        return 'main'
    
    import views
    app.register_blueprint(views.bp)
    

    return app

app = create_app()


if __name__ == '__main__':
    # app.run(ssl_context='adhoc')
    app.run()
