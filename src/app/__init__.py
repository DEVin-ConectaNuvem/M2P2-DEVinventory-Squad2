import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from src.app.config import app_config


db = SQLAlchemy()
ma = Marshmallow()


def create_app():

    app = Flask(__name__)
    
    app.config.from_object(app_config[os.getenv('FLASK_ENV')])
    db.init_app(app)
    ma.init_app(app)
    Migrate(app=app, db=db, directory='./src/app/migrations')
    CORS(app)

    return app
