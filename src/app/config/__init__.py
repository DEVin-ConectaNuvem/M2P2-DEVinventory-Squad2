import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

NAME_DB = os.getenv('NAME_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET')
    TOKEN_EXPIRE_HOURS = os.getenv('TOKEN_EXPIRE_HOURS')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
    BACKEND_URL = os.getenv('BACKEND_URL')
    FRONTEND_URL = os.getenv('FRONTEND_URL')


class Development(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}-development"

class Testing(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}-testing"

class Homologation(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}-homologation"

class Production(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}-production"

app_config = { 
    "development": Development,
    "production": Production, 
    "testing": Testing, 
    "homologation": Homologation 
}
