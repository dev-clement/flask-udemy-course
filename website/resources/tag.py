from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from website.db import db
from website.models import TagModel, StoreModel, ItemModel
from website.resources.schema import TagSchema, TagAndItemSchema

blp = Blueprint('Tags', "tags", description='Operations on tags')

@blp.route('/store/<string:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id).first():
            abort(400, message='A tag with that name already exists in that store...')
        
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commi()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return tag

@blp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(tag)
            db.session.commi()
        except SQLAlchemyError:
            abort(http_status_code=500, message='An error occured while inserting the tag...')
        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(http_status_code=500, message='An error occured while inserting the tag')
        return {'message': 'Item removed from tag', 'item': item, 'tag': tag}

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202, description='Deletes a tag if no item is tagged whith it...', example={'message': 'Tag removed.'})
    @blp.alt_response(404, description='Tag not found...')
    @blp.alt_response(400, description='Returned if the tag is assigned to one or more items. In that case, the tag is not removed')
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'Tag removed...'}
        abort(400, message='Could not removed the tag. Make sure that no-item is related to it...')
