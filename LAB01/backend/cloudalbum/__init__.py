"""
    cloudalbum/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Environment configuration how to run application.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""

import os
import logging
import sys
import json
import datetime
from bson.objectid import ObjectId
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import Conflict

# instantiate the database
db = SQLAlchemy()


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def create_app(script_info=None):

    # instantiate the application
    app = Flask(__name__)

    # initiate some config value for JWT Authentication
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'my_jwt')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    # initiate some config value for JWT Authentication
    jwt = JWTManager(app)
    app.json_encoder = JSONEncoder

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # set config
    app_settings = os.getenv('APP_SETTINGS', 'cloudalbum.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    # set logger to STDOUT
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.DEBUG)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from cloudalbum.api.users import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from cloudalbum.api.photos import photos_blueprint
    app.register_blueprint(photos_blueprint, url_prefix='/photos')

    from cloudalbum.api.admin import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Setup models for DB operations
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Create database tables')
        except Exception as e:
            app.logger.error(e)


    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist_set(decrypted_token):
        from cloudalbum.util.jwt_helper import is_blacklisted_token_set
        try:
            return is_blacklisted_token_set(decrypted_token)
        except Exception as e:
            app.logger.error(e)
            raise Conflict('Session already expired: {0}'.format(e))


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'application': app, 'database': db}

    return app
