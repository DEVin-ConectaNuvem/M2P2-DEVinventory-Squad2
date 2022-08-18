from flask import Blueprint, jsonify

from src.app.models.user import User, users_share_schema
from src.app.models.inventory import Inventory, intentories_share_schema


inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory.route("/", methods = ['GET'])
def list_all_requirements():

    users_db_data = User.quey.all()
    inventory_db_data = Inventory.query.all()

    users_dict = users_share_schema.dump(users_db_data)
    inventory_dict = intentories_share_schema.dump(inventory_db_data)

    print(users_dict)
    # print(inventory_dict)



'''
- Calcular o número de usuários.
- Calcular o número de itens.
- Calcular o valor da soma de todos os itens.
- Calcular quantos itens estão emprestados para usuários.
- Retornar às estatísticas, além do Status 200 (OK)
'''