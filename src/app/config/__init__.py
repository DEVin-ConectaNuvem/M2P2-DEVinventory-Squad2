import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
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


class Testing(Config):
    DEBUG = False
    TESTING = True


class Homologation(Config):
    DEBUG = False
    TESTING = False


class Production(Config):
    DEBUG = False
    TESTING = False


app_config = { "development": Development, "production": Production, "testing": Testing, "homologation": Homologation }
