from flask import Blueprint, jsonify, request
from flask import json
from flask.wrappers import Response
from src.app import db
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


@user.route("/<int:users>", methods = ['PATCH'])
@requires_access_level(['UPDATE'])
@validate_body(user_schemas.UpdateUserBodySchema())
def atualiza_user(users, body):

        usuario_objeto = User.query.filter_by(id=users).first()
        
           
        if body['age'] !='' and usuario_objeto:
            usuario_objeto.age = body['age']
        if body['city_id'] !='' and usuario_objeto:
            usuario_objeto.city_id = body['city_id']
        if body['complement'] !='' and usuario_objeto:
            usuario_objeto.complement = body['complement']
        if body['district'] !='' and usuario_objeto:
            usuario_objeto.district = body['district']
        if body['email'] !='' and usuario_objeto:
            usuario_objeto.email = body['email']
        if body['gender_id'] !='' and usuario_objeto:
            usuario_objeto.gender_id = body['gender_id']
        if body['landmark'] !='' and usuario_objeto:
            usuario_objeto.landmark = body['landmark']                
        if  body['name'] !='' and usuario_objeto:
            usuario_objeto.name = body['name']
        if  body['number_street'] !='' and usuario_objeto:
            usuario_objeto.number_street = body['number_street']
        if  body['street'] !='' and usuario_objeto:
            usuario_objeto.street = body['street']
        if  body['cep'] !='' and usuario_objeto:
            usuario_objeto.cep = body['cep']
        if  body['number_street'] !='' and usuario_objeto:
            usuario_objeto.number_street = body['number_street']
        if  body['password'] !='' and usuario_objeto:
            usuario_objeto.password = User.encrypt_password(body['password'].encode("utf-8"))
        if  body['phone'] !='' and usuario_objeto:
            usuario_objeto.phone = body['phone']
        if  body['role_id'] !='' and usuario_objeto:
            usuario_objeto.role_id = body['role_id']
        
              
      
        if usuario_objeto:    
           db.session.add(usuario_objeto) 
           db.session.commit()
           return jsonify({"Message": "Usuário atualizado com sucesso."}), 204

        
        return jsonify({"error": "Usuário não encontrado."}), 404
    

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

