from datetime import datetime, timedelta
from flask import jsonify
from src.app.models.user import User
from src.app.models.user import User, user_share_schema
from src.app.utils import generate_jwt

def create_user(gender_id, city_id, role_id, name, age, email,\
    phone, password, cep,\
    district, street, number_street, complement, landmark):

    try:
        User.seed(
            gender_id=gender_id, 
            city_id=city_id,
            role_id=role_id, 
            name=name, 
            age=age, 
            email=email,
            phone=phone, 
            password=password, 
            cep=cep,
            district=district, 
            street=street, 
            number_street=number_street, 
            complement=complement,
            landmark=landmark
        )

        return {"message": "Usuário criado com sucesso."}

    except:
        return {"error": "Erro na criação de Usuário. Verifique os dados novamente."}


def make_login(email, password):

    try:

        user_query = User.query.filter_by(email = email).first_or_404()
        user = user_share_schema.dump(user_query)

        if not user_query.check_password(password):
            return {"error": "Dados inválidos", "status_code": 401}

        payload = {
            "name": user['name'],
            "user_id": user_query.id,
            "exp": datetime.utcnow() + timedelta(days=1),
            "roles": user["role_id"]
        }

        token = generate_jwt(payload)

        return {"token": token}
    except:
        return {"error": "Ops! Algo deu errado...", "status_code": 500}


def get_by_id(id):
    user = User.query.filter(User.id==id).first()
    
    
    return user_share_schema.dump(user)