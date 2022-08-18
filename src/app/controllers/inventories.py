from flask import Blueprint, jsonify

from src.app.models.user import User, users_share_schema
from src.app.models.inventory import Inventory, intentories_share_schema


inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory.route("/results", methods = ['GET'])
def list_all_requirements():

    users_db_data = User.query.all()
    inventory_db_data = Inventory.query.all()
    inventory_dict = intentories_share_schema.dump(inventory_db_data)

    total_users = len(users_db_data)
    total_items = len(inventory_dict)

    total_items_price = 0
    total_items_loaned = 0
    for item in inventory_dict:
        print(item)
        if item['user_id'] != None:
            total_items_loaned += 1
        elif item['value'] > 0 and item['value'] != None:
            total_items_price += item['value']

    return_dados = {
        'total_items': total_items, 
        'total_users': total_users, 
        'total_items_loaned': total_items_loaned,
        'total_items_price': total_items_price
        }

    return jsonify(return_dados), 200
