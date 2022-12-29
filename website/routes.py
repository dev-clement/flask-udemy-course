import uuid
from flask import Blueprint, jsonify, request
from .models import stores, items
from flask_smorest import abort

bp = Blueprint('bp', __name__)

@bp.route('/store', methods=['GET'])
def get_stores():
    return {'stores': list(stores.values())}

@bp.route('/item', methods=['GET'])
def get_item():
    return {"items": list(items.values())}


@bp.route('/item/<string:item_id>')
def get_item_in_store(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Store not found...")

@bp.route('/store/<string:store_id>', methods=['GET'])
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found...")

@bp.route('/store', methods=['POST'])
def create_store():
    store_data = request.get_json()
    if 'name' not in store_data:
        abort(400, message="Bad request. Endure 'name' is included in the JSON payload")
    for store in stores.values():
        if store_data['name'] == store['name']:
            abort(400, message=f'''Store {store['name']} already exists...''')
    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id}
    stores[store_id] = store
    return store

@bp.route('/item', methods=['POST'])
def create_item():
    item_data = request.get_json()
    if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Endure price, store_id and name are present in the payload")
    for item in items.values():
        if item_data['name'] == item['name'] and item_data['store_id'] == item['store_id']:
            abort(400, message=f'''Item {item['name']} already exists''')
    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item
    return item, 201

@bp.route('/item/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": f"The item {item_id} gets deleted"}
    except KeyError:
        abort(404, message=f"The item {item_id} is not found...")

@bp.route('/item/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price' and 'name' are present in the request")
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found...")

@bp.route('/store/<string:store_id>', methods=['DELETE'])
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message': f"Store {store_id} is deleted..."}
    except KeyError:
        abort(404, message=f"Store {store_id} not found...")
