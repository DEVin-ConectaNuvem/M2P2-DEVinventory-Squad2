from flask import Blueprint, jsonify, request

from src.app.models.user import User, users_roles_share_schema

user = Blueprint('user', __name__, url_prefix='/user')

@user.route("/", methods = ['GET'])
def list_user():
    
    list_users = User.query.paginate(per_page=20, error_out=True)

    list_users_dict = users_roles_share_schema.dump(list_users.items)

    return jsonify(list_users_dict), 200

@user.route("/<string:name>", methods = ['GET'])
def list_user_by_name(name):

    name_cap = name.capitalize()

    list_name_user = User.query.filter(User.name.like(f"%{name_cap}%")).all()

    list_name_dict = users_roles_share_schema.dump(list_name_user)

    if list_name_dict == []:
        return jsonify({"message": "Usuário não encontrado"}), 204

    return jsonify(list_name_dict), 200
