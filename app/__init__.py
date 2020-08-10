from flask import Flask

from config import BaseConfig
from app.extensions import bcrypt, login_manager
from app.database import db
from app.blueprints.core import core as core_blueprint
from app.blueprints.user import user as user_blueprint


def create_app(config=BaseConfig):
    app = Flask(__name__)


    if app.config['ENV'] == 'production':
        app.config.from_object('config.BaseConfig')
    if app.config['ENV'] == 'development':
        app.config.from_object('config.TestConfig')
    if app.config['ENV'] == 'testing':
        app.config.from_object('config.AuthTestConfig')


    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user_blueprint)
    app.register_blueprint(core_blueprint)
