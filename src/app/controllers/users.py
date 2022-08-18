from flask import Blueprint, jsonify, request

from src.app.models.user import User, users_share_schema

user = Blueprint('user', __name__, url_prefix='/user')

@user.route("/", methods = ['POST'])
def list_user():
    
    data = request.get_json()

    list_users = User.query.all()

    list_users_dict = users_share_schema.dump(list_users)

    if data['name'] == "":
        
        return jsonify(list_users_dict), 200


    return jsonify(data), 200


