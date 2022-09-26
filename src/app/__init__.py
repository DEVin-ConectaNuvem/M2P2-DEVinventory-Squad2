from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from src.app.config import app_config

db = SQLAlchemy()
ma = Marshmallow()


def create_app(environment):

    app = Flask(__name__)
    
    app.config.from_object(app_config[environment])
    db.init_app(app)
    ma.init_app(app)
    Migrate(app=app, db=db, directory='./src/app/migrations')
    CORS(app)
    app.config['Access-Control-Allow-Origin'] = '*'
    app.config["Access-Control-Allow-Headers"]="Content-Type"

    from src.app.models import country, state, city, permission, role, gender, user, product_category, inventory

    return app
