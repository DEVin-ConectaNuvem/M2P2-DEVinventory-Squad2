from flask import Blueprint, jsonify, request


from src.app.middlewares.auth import requires_access_level
from src.app.models.inventory import Inventory, intentories_share_schema
from src.app.models.user import User
from src.app.services.inventory_services import create_product
from src.app.utils import allkeys_in, exist_product_code 


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
        if item['user_id'] != None:
            total_items_loaned += 1
        if item['value'] > 0 and item['value'] != None:
            total_items_price += item['value']

    return_dados = {
        'total_items': total_items, 
        'total_users': total_users, 
        'total_items_loaned': total_items_loaned,
        'total_items_price': round(total_items_price, 2)
        }

    return jsonify(return_dados), 200

@inventory.route("/create", methods= ["POST"])
@requires_access_level("WRITE")
def create():
    
    list_keys = ["product_category_id", "product_code", "title", "value", "brand", "template", "description"]
    
    data = allkeys_in(request.get_json(), list_keys)
    if 'error' in data:
        return {"error": data}, 401
    
    if exist_product_code(data, inventory):
        return jsonify({"error": "Esse código de produto já existe"}), 400
    
    if data["value"] <= 0:
        return jsonify({"error": "O valor não pode ser menor ou igual a zero"}), 400
    
    if "user_id" not in data.keys():
        data['user_id'] = None
        
    response = create_product(
        product_category_id = data["product_category_id"],
        user_id = data["user_id"],
        product_code = data["product_code"],
        title = data["title"], 
        value = data["value"], 
        brand = data["brand"], 
        template = data["template"], 
        description = data["description"]
    )
    
    if "error" in response:
        return jsonify(response), 400
    
    return jsonify(response), 201
