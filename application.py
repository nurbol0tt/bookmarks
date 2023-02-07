from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate

from config.prod_config import ProductConfig
from models.user_models.models import db

# from core.domain.account.entity.account import db

from extenstions.exception_extension import register_exception_handler
from extenstions.routes_extension import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductConfig)

    JWTManager(app)
    db.init_app(app)
    Migrate(app, db)
    Mail(app)
    Bcrypt(app)

    register_routes(app)
    register_exception_handler(app)

    return app
