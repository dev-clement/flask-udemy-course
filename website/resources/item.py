import uuid
from sqlalchemy.exc import SQLAlchemyError
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from website.models import item
from website.resources.schema import ItemSchema, ItemUpdateSchema
from website.models import ItemModel
from website.db import db

blp = Blueprint('Items', 'items', description='Operation on items')

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self, item_id):
        return ItemModel.query.all()
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        return {'message': 'Item get removed'}, 200
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()
    
        return item

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return item.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(http_status_code=500, message='An error occured while inserting the item...')
        return item