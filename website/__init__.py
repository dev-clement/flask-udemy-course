import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from .db import db
from .resources.item import blp as ItemBlueprint
from .resources.store import blp as StoreBlueprint
from . import models

def create_app(db_url = None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ThisIsSecret'
    app.config['PROPAGATE_EXCEPTION'] = True
    app.config['API_TITLE'] = 'Stores REST API'
    app.config['API_VERSION'] = '1.0.0'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config[
        'OPENAPI_SWAGGER_UI_URL'
    ] = 'https://cdn.jsdeliver.net/npm/swagger-ui-dist/'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
