from flask import Blueprint

user = Blueprint('user', __name__, url_prefix='/user')

@user.route("/", methods = ['GET'])
def list_user():
    return "<p>Lista de usuários!</p>"
