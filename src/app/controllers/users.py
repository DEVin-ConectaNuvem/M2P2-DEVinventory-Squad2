from flask import Blueprint, jsonify, request
from flask import json
from flask.wrappers import Response
from src.app.services.user_services import make_login
from src.app.utils import allkeys_in


from src.app.models.user import User #, teste_users_schema

user = Blueprint('user', __name__, url_prefix='/user')

# @user.route("/", methods = ['GET'])
# def list_user():
    
#     list_users = User.query.all()

#     list_users_dict = teste_users_schema.dump(list_users)

    # if data == {}:
    #     return jsonify(list_users_dict), 200

    # if data['name'] == "":
        
    #     return jsonify(list_users_dict), 200


    # return jsonify(list_users_dict), 200

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



