from flask import current_app
from jwt import encode
import random


def allkeys_in(request_json, keys_list):
    missing_keys = []
    for key in range(len(keys_list)):
        if keys_list[key] not in request_json:
            missing_keys.append(keys_list[key])
            
    if len(missing_keys) > 0:
        return {"error": f"Está faltando o(s) item(s) {missing_keys}"}

    return request_json


def generate_jwt(payload):
    token = encode(payload, current_app.config['SECRET_KEY'], 'HS256')
    return token


def gera_password(): 
    letras = "abcdefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ123456789"
    caracter = '!@#$%&^*-_'

    password = ""

    for i in range(0, 1):
        password_caracter = random.choice(caracter)
        password += password_caracter
        for h in range(0, 14):
            password_letras = random.choice(letras)
            password += password_letras
    return password

def exist_product_code(body, data_in_db):

    for json in data_in_db:
        if json['product_code'] == body['product_code']:
            return True

    return False

