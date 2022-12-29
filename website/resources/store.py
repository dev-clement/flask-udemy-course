import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from website.models import stores
from .schema import StoreSchema

blp = Blueprint('stores', __name__, description='Operations on stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='Store not found...')

    def delete(cls, store_id):
        try:
            del stores[store_id]
        except KeyError:
            abort(404, message='Store not found...')

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store['name'] == store_data['name']:
                abort(400, message=f"Store {store_data['name']} already exists")
        store_id = uuid.uuid4().hex
        store = {**store_data, 'id': store_id}
        stores[store_id] = store
        return store


