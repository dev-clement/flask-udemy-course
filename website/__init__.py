import os
import uuid
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_migrate import Migrate
from .db import db
from .resources.users import blp as UserBlueprint
from .resources.item import blp as ItemBlueprint
from .resources.store import blp as StoreBlueprint
from .resources.tag import blp as TagBlueprint
from . import models
from .models.item import ItemModel
from .models.tag import TagModel
from .models.store import StoreModel
from .models.item_tags import ItemTag
from .blocklist import BLOCKLIST
from flask_jwt_extended import JWTManager

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
    app.config['JWT_SECRET_KEY'] = uuid.uuid4().hex
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    jwt = JWTManager(app=app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        return {'id_admin': True if identity == 1 else False}

    @jwt.expired_token_loader
    def expired_token_callback(error):
        return (jsonify({'message': 'The token has expired', 'error': 'token_expired'}), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({'message': 'Signature verification failed...', 'error': 'invalid_token'}), 401)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({'description': 'Request does not contain an access token...', 'error': 'authorization_required'}), 401)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({'description': 'The token has been revoked', 'error': 'token_revoked'})), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({'description': 'The token is not fresh anymore', 'error': 'fresh_token_required'})), 401

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
