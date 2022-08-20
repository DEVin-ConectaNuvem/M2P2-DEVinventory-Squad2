from flask import Blueprint, jsonify, request
from src.app.models.user import User, users_roles_share_schema, users_share_schema
from src.app  import db as Banco
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

@user.route("/<int:users>", methods = ['PATCH'])
def atualiza_user(users):

        usuario_objeto = User.query.filter_by(id=users).first()
        body = request.get_json()
            
    

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
        

        new_user = User(body['gender_id'],body['role_id'],body['city_id'],body['name'],body['age'],body['email'],body['password'],body['phone'],body['cep'],body['street'],body['number_street'],body['complement'],body['landmark'],body['district'])
        print(new_user)
            
      
        if usuario_objeto:    
           Banco.session.add(usuario_objeto) 
           Banco.session.commit()
           return jsonify('Sucesso'), 204

        
        return "Não encontrado", 404
    


