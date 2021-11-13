from flask import Flask
import app.exceptions as app_exception
from flask_jwt_extended import JWTManager
from app.extentions import db

def register_error_handlers(app):
    app.register_error_handler(400, app_exception.page_not_found)
    app.register_error_handler(500, app_exception.server_error)


app = Flask(__name__)
app.config.from_object('config.DevConfig')
register_error_handlers(app)

from app.users import users
app.register_blueprint(users)
jwt_manager = JWTManager(app)

