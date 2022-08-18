from flask import Blueprint, jsonify, request

from src.app.models.user import User, users_roles_share_schema

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

