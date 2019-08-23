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
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_jwt_extended import JWTManager


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

# instantiate the database
db = SQLAlchemy()
login = LoginManager()
jwt = JWTManager()


def create_app(script_info=None):

    # instantiate the application
    app = Flask(__name__)

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

    # Setup models for DB operations
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Create database tables')
        except Exception as e:
            app.logger.error(e)


    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist_set(decrypted_token):
        from project.util.jwt_helper import is_blacklisted_token_set
        try:
            return is_blacklisted_token_set(decrypted_token)
        except Exception as e:
            app.logger.error(e)
            return make_response(jsonify({'msg': 'session already expired'}, 409))


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'application': app, 'database': db}

    return app
