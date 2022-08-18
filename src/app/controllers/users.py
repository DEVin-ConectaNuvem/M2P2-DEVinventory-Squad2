from flask import Blueprint, jsonify, request

from src.app.models.user import User, teste_users_schema

user = Blueprint('user', __name__, url_prefix='/user')

@user.route("/", methods = ['POST'])
def list_user():
    
    list_users = User.query.all()

    list_users_dict = teste_users_schema.dump(list_users)

    # if data == {}:
    #     return jsonify(list_users_dict), 200

    # if data['name'] == "":
        
    #     return jsonify(list_users_dict), 200


    return jsonify(list_users_dict), 200


