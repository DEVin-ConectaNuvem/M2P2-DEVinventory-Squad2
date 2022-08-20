from types import NoneType
from flask import Blueprint, jsonify, request
from flask import json
from flask.wrappers import Response
from src.app.services.user_services import make_login
from src.app.services.user_services import create_user
from src.app.utils import allkeys_in
from src.app.middlewares.auth import requires_access_level
from src.app.models.user import User, users_roles_share_schema
from src.app.models.city import City
from src.app.models.gender import Gender
from src.app.models.role import Role
from src.app.utils.decorators import validate_body
from src.app.schemas import user_schemas


user = Blueprint('user', __name__, url_prefix='/user')


@user.route("/", defaults={"users": 1})
@user.route("/<int:users>", methods=['GET'])
@user.route("/<string:users>", methods=['GET'])
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

@user.route("/create", methods=['POST'])
@validate_body(user_schemas.CreateUserBodySchema())
def post_create_users(data):


    if not Gender.query.filter(Gender.id==data['gender_id']).first():
        return jsonify({'error': 'Gênero não existente.'}), 404

    if not City.query.filter(City.id==data['city_id']).first():
        return jsonify({'error': 'Cidade não existente.'}), 404

    if not Role.query.filter(Role.id==data['role_id']).first():
        return jsonify({'error': 'Cargo não existente.'}), 404

    if 'complement' not in data:
        data['complement'] = None

    if 'landmark' not in data:
        data['landmark'] = None

    response = create_user(**data)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 201

@user.route("/login", methods=['POST'])
def user_login():

    data = request.get_json()
    keys_list = ['email', 'password']
    check_keys = allkeys_in(data, keys_list)

    if 'error' in check_keys:
        return {"error": check_keys}, 401

    response = make_login(data['email'], data['password'])

    if "error" in response:

        return Response(
        response= json.dumps({"error": response['error']}),
        status=response['status_code'],
        mimetype='application/json'
        )

    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
