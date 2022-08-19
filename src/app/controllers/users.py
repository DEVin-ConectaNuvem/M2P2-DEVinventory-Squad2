from flask import Blueprint, jsonify, request

from src.app.models.user import User, users_roles_share_schema
from src.app.services.user_services import create_user
from src.app.utils import exists_key

user = Blueprint('user', __name__, url_prefix='/user')

@user.route("/", defaults = {"users": 1})
@user.route("/<int:users>", methods = ['GET'])
@user.route("/<string:users>", methods = ['GET'])
def list_user_per_page(users):
    
    if type(users) == str:

        list_name_user = User.query.filter(User.name.ilike(f"%{users}%")).all()

        list_name_dict = users_roles_share_schema.dump(list_name_user)

        if list_name_dict == []:

            error = {
                "Error": "Usuário não encontrado."
            }

            return jsonify(error), 204

        return jsonify(list_name_dict), 200

    list_users = User.query.paginate(per_page=20, page=users, error_out=True)

    list_users_dict = users_roles_share_schema.dump(list_users.items)

    return jsonify(list_users_dict), 200

@user.route("/create", methods = ['POST'])
def post_create_users():
    
    list_keys = ['gender_id', 'city_id', 'role_id', 'name', 'age', 'email',\
        'phone', 'password', 'cep', 'district', \
        'street', 'number_street']

    data = exists_key(request.get_json(), list_keys)

    if 'complement' not in data:
        data['complement'] = None

    if 'landmark' not in data:
        data['landmark'] = None
    
    if "error" in data:
        return jsonify(data), 400
    
    response = create_user(
        gender_id=data['gender_id'], 
        city_id=data['city_id'], 
        role_id=data['role_id'], 
        name=data['name'],
        age=data['age'],
        email=data['email'],
        phone=data['phone'], 
        password=data['password'],
        cep=data['cep'],
        district=data['district'], 
        street=data['street'], 
        number_street=data['number_street'],
        complement=data['complement'],
        landmark=data['landmark']
    )

    if "error" in response:
        return jsonify(response), 400
    

    return jsonify(response), 201

