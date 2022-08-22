from flask import Blueprint, jsonify, request

from src.app import db
from src.app.models.inventory import Inventory
from src.app.middlewares.auth import requires_access_level
from src.app.services.inventory_services import create_product, get_all_inventories, get_inventories_by_name
from src.app.utils import exist_product_code
from src.app.services.queries_services import queries
from src.app.schemas.product_schema import ProductBodySchema, UpdateProductBodySchema
from src.app.utils.decorators import validate_body


inventory = Blueprint('inventory', __name__, url_prefix='/inventory')


@inventory.route("/results", methods = ['GET'])
@requires_access_level(["READ"])
def list_all_requirements():

    users_db_data = queries(model='user', type_request='all')
    inventory_db_data = queries(model='inventory', type_request='all', schema='inventories')

    total_items_price = 0
    total_items_loaned = 0
    for item in inventory_db_data:
        if item['user_id'] != None:
            total_items_loaned += 1
        if item['value'] > 0 and item['value'] != None:
            total_items_price += item['value']

    return_dados = {
        'total_items': len(inventory_db_data),
        'total_users': len(users_db_data),
        'total_items_loaned': total_items_loaned,
        'total_items_price': round(total_items_price, 2)
        }

    return jsonify(return_dados), 200


@inventory.route("/create", methods= ["POST"])
@validate_body(ProductBodySchema())
@requires_access_level(["WRITE"])
def create(body):

    if exist_product_code(body['product_code']):
        return jsonify({"error": "Esse código de produto já existe"}), 400

    if not body["value"]:
        return jsonify({"error": "O valor não pode ser menor ou igual a zero"}), 400

    response = create_product(**body)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 201


@inventory.route('/', methods=['GET'])
@requires_access_level(["READ"])
def get_inventories():
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)
    
    if name:
        inventories_by_name = get_inventories_by_name(name, page=page)
        
        if not inventories_by_name:
            return jsonify(), 204

        return jsonify(inventories_by_name), 200
    
    all_inventories = get_all_inventories(page)
    
    if not all_inventories:
            return jsonify(), 204
    
    return jsonify(all_inventories), 200


@inventory.route("/<int:id>", methods = ["PATCH"])
@requires_access_level(['UPDATE'])
@validate_body(UpdateProductBodySchema())
def update_item(id, body):

    try:
        Inventory.query.filter_by(id=id).first_or_404()

        Inventory.query.filter_by(id=id).update(body)
        db.session.commit()
        return jsonify({"Message": "Item atualizado com sucesso."}), 204
    except:
        return jsonify({"error": 'Item não encontrado.'}), 404
