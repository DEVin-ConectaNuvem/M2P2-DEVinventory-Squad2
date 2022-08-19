from functools import wraps
from jwt import decode
from flask import current_app, request, jsonify
from src.app.models.user import User
from src.app.models.role import Role, role_share_schema


def requires_access_level(permissions):

    def jwt_required(function_current):

        @wraps(function_current)
        def wrapper(*args, **kwargs):

            token = None

            if "Authorization" in request.headers:
                token = request.headers["Authorization"]

            if not token:
                return jsonify({"error": "Você não tem permissão"}), 403

            if not "Bearer" in token:
                return jsonify({"error": "Você não tem permissão"}), 401

            try:
                token_pure = token.replace("Bearer ", "")
                decoded = decode(token_pure, current_app.config["SECRET_KEY"],
                                 "HS256")

                current_user = User.query.get(decoded['user_id'])

            except Exception:
                return jsonify({"error": "O Token é inválido"}), 403

            current_role = Role.query.get(current_user.role.id)
            role_permissions = role_share_schema.dump(current_role)['permissions']

            roles = [permission['description'] for permission in role_permissions if permission['description']  in permissions]

            if len(roles) < len(permissions):
                return jsonify({
                    "error":
                    "Você não tem permissão para essa funcionalidade"
                }), 403

            return function_current(*args, **kwargs)

        return wrapper

    return jwt_required
