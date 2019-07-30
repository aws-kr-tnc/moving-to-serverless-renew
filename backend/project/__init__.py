import os
import logging
import sys

from flask import Flask  # new
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# instantiate the db
db = SQLAlchemy()
login = LoginManager()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set logger to STDOUT
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.DEBUG)

    # set up extensions
    db.init_app(app)
    login.init_app(app)

    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    from project.api.photos import photos_blueprint
    app.register_blueprint(photos_blueprint)

    from project.api.map import map_blueprint
    app.register_blueprint(map_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
