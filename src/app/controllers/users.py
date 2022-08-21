import requests
from flask import Blueprint, jsonify, request, current_app
from flask import json
from flask.wrappers import Response
from werkzeug.utils import redirect
from flask.globals import session
from google_auth_oauthlib.flow import Flow
from google import auth 
from google.oauth2 import id_token 
from src.app import db
from src.app.services.user_services import make_login, create_user, get_user_by_email
from src.app.utils import allkeys_in, generate_jwt, gera_password
from src.app.middlewares.auth import requires_access_level
from src.app.models.user import User, users_roles_share_schema
from src.app.models.city import City
from src.app.models.gender import Gender
from src.app.models.role import Role
from src.app.utils.decorators import validate_body
from src.app.schemas import user_schemas
from sqlalchemy.exc import IntegrityError


user = Blueprint('user', __name__, url_prefix='/user')


# flow = Flow.from_client_secrets_file(
#     client_secrets_file="src/app/database/client_secret.json",
#     scopes=[
#         "https://www.googleapis.com/auth/userinfo.email",
#         "https://www.googleapis.com/auth/userinfo.profile",
#         "openid"
#     ],
#     redirect_uri = "http://localhost:5000/user/callback"
# )


@user.route("/", defaults={"users": 1})
@user.route("/<int:users>", methods=['GET'])
@user.route("/<string:users>", methods=['GET'])
@requires_access_level(['READ'])
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


@user.route("/<int:id>", methods = ['PATCH'])
# @requires_access_level(['UPDATE'])
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

    if not Gender.query.filter(Gender.id==body['gender_id']).first():
        return jsonify({'error': 'Gênero não existente.'}), 404

    if not City.query.filter(City.id==body['city_id']).first():
        return jsonify({'error': 'Cidade não existente.'}), 404

    if not Role.query.filter(Role.id==body['role_id']).first():
        return jsonify({'error': 'Cargo não existente.'}), 404

    if 'complement' not in body:
        body['complement'] = None

    if 'landmark' not in body:
        body['landmark'] = None

    response = create_user(**body)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 201


@user.route("/login", methods=['POST'])
def user_login():

    data = request.get_json()
    keys_list = ['email', 'password']
    check_keys = allkeys_in(data, keys_list)

    if 'error' in check_keys:
        return {"error": check_keys}, 400

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
