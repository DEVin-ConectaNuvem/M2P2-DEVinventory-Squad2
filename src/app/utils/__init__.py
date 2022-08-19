from flask import current_app
from jwt import encode

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

