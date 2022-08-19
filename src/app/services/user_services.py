from datetime import datetime, timedelta
from src.app.models.user import User, user_share_schema
from src.app.utils import generate_jwt


def make_login(email, password):

    try:

        user_query = User.query.filter_by(email = email).first_or_404()
        user = user_share_schema.dump(user_query)

        if not user_query.check_password(password):
            return {"error": "Dados inválidos", "status_code": 401}
        
        payload = {
            "name": user['name'],
            "email": user['email'],
            "exp": datetime.utcnow() + timedelta(days=1)
        }

        token = generate_jwt(payload)

        return {"token": token}
    except:
        return {"error": "Ops! Algo deu errado...", "status_code": 500}


