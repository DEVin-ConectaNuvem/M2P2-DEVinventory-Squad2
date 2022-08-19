from flask import jsonify

from src.app.models.user import User


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
        return {"error": "Erro na criação de Usuário."}

