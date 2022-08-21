from flask import current_app
from jwt import encode
from google_auth_oauthlib.flow import Flow
import random

from src.app.models.inventory import Inventory


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

def exist_product_code(body):
    if Inventory.query.filter_by(product_code=body).first():
        return True
    return False


flow = Flow.from_client_secrets_file(
    client_secrets_file="src/app/database/client_secret.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ],
    redirect_uri = "http://localhost:5000/user/callback"
)
