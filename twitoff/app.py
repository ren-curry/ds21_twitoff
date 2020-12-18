"""
Main app/routing file for Twitoff
"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User

from twitoff.routes.home_routes import home_routes
from twitoff.routes.prediction_routes import prediction_routes
from twitoff.routes.data_routes import data_routes


def create_app():
    app = Flask(__name__)

    # Configurations
    app.config["SECRET_KEY"] = getenv('SECRET_KEY', default="super secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('APP_DB_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    app.register_blueprint(home_routes)
    app.register_blueprint(prediction_routes)
    app.register_blueprint(data_routes)

    return app
