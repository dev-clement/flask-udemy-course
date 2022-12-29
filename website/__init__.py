from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from .resources.item import blp as ItemBlueprint
from .resources.store import blp as StoreBlueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ThisIsSecret'
    app.config['PROPAGATE_EXCEPTION'] = True
    app.config['API_TITLE'] = 'Stores REST API'
    app.config['API_VERSION'] = '1.0.0'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_URL'] = 'https://cdn.jsdeliver.net/npm/swagger-ui-dist/'

    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
