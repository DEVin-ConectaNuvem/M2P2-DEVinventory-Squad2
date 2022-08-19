from flask import Flask

from src.app.controllers.users import user
from src.app.controllers.inventories import inventory


def routes(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(inventory)
