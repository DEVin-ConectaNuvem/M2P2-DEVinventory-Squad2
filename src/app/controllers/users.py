import requests
from flask import Blueprint, jsonify, request, current_app
from flask import json
from sqlalchemy.exc import IntegrityError
from flask.wrappers import Response
from werkzeug.utils import redirect
from flask.globals import session

from google import auth 
from google.oauth2 import id_token 
from src.app import db
from src.app.services.user_services import make_login, create_user, get_user_by_email
from src.app.utils import generate_jwt, gera_password
from src.app.middlewares.auth import requires_access_level
from src.app.models.user import User
from src.app.models.city import City
from src.app.models.gender import Gender
from src.app.models.role import Role
from src.app.utils.decorators import validate_body
from src.app.schemas import user_schemas
from src.app.services.user_services import get_users_by_name, get_all_users
from src.app.services.queries_services import check_existence
from src.app.utils import flow


user = Blueprint('user', __name__, url_prefix='/user')


@user.route("/", methods=['GET'])
@requires_access_level(['READ'])
def list_user_per_page():

    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)

    if name:

        list_name_user = get_users_by_name(name, page)

        if not list_name_user:
            error = {
                "Error": "Usuário não encontrado."
            }
            return jsonify(error), 204

        return jsonify(list_name_user), 200

    list_users = get_all_users(page)

    return jsonify(list_users), 200


@user.route("/<int:id>", methods = ['PATCH'])
@requires_access_level(['UPDATE'])
@validate_body(user_schemas.UpdateUserBodySchema())
def update_user(id, body):
        try:
            User.query.filter_by(id=id).first_or_404()
    
            User.query.filter_by(id=id).update(body)
          
            db.session.commit()
        
            return jsonify({"Message": "Usuário atualizado com sucesso."}), 204

        except IntegrityError:
            return jsonify({"error": 'Email já existe.'}), 409
        
        except Exception:
            return jsonify({"error": 'Usuário não existe.'}), 404
        
    

@user.route("/create", methods=['POST'])
@requires_access_level(['READ', 'WRITE', 'UPDATE', 'DELETE'])
@validate_body(user_schemas.CreateUserBodySchema())
def post_create_users(body):

    models = [
            {'model': Gender, 'id': body['gender_id']}, 
            {'model': City,'id': body['city_id']},
            {'model': Role, 'id':body['role_id']}
        ]

    if not all([check_existence(model['model'], model['id'])for model in models]):
        return jsonify({'error': 'Algum dos IDs não foi encontrado.'}), 404

    response = create_user(**body)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 201


@user.route("/login", methods=['POST'])
@validate_body(user_schemas.LoginBodySchema())
def user_login(body):

    response = make_login(body['email'], body['password'])

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


@user.route('/auth/google', methods = ["POST"])
def auth_google():

    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return Response(
        response=json.dumps({'url':authorization_url}),
        status=200,
        mimetype='application/json'
    )  


@user.route('/callback', methods = ["GET"])
def callback():

    flow.fetch_token(authorization_response = request.url)
    credentials = flow.credentials
    request_session = requests.session()
    token_google = auth.transport.requests.Request(session=request_session)

    user_google_dict = id_token.verify_oauth2_token(
        id_token = credentials.id_token,
        request=token_google,
        audience=current_app.config['GOOGLE_CLIENT_ID']
    )

    user = get_user_by_email(user_google_dict['email'])

    password_gerado = gera_password()

    if "error" in user:
        user = create_user(
            gender_id=None, 
            city_id=None,
            role_id=3, 
            name=user_google_dict['name'], 
            age=None, 
            email=user_google_dict['email'],
            phone=None, 
            password=password_gerado, 
            cep=None,
            district=None, 
            street=None, 
            number_street=None,
            complement=None,
            landmark=None
        )
        user = get_user_by_email(user_google_dict['email'])

    user_google_dict["user_id"] = user['id']
    user_google_dict["role"] = user['role']

    session["google_id"] = user_google_dict.get("sub")

    del user_google_dict['aud']
    del user_google_dict['azp']

    token = generate_jwt(user_google_dict)

    return redirect(f"{current_app.config['FRONTEND_URL']}?jwt={token}")
