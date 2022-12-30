from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from website.db import db
from website.models import StoreModel
from website.resources.schema import StoreSchema

blp = Blueprint('Stores', 'stores', description='Operations on stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(cls, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {'message': 'The store is removed'}, 200

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(http_status_code=400, message='A store with that name already exists, please take another one...')
        except SQLAlchemyError:
            abort(http_status_code=500, message='An error occured while creating the store...')
        return store


