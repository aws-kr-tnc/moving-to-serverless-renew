import os
import logging
import sys
import json
import datetime

from bson.objectid import ObjectId
from flask import Flask, jsonify, make_response  # new
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

# instantiate the db
db = SQLAlchemy()
login = LoginManager()
jwt = JWTManager()


def create_app(script_info=None):

    # instantiate the app
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

    from cloudalbum.api.map import map_blueprint
    app.register_blueprint(map_blueprint)

    # Setup models for DB operations
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(e)


    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist_DB(decrypted_token):
        from cloudalbum.util.blacklist_helper import is_blacklisted_token_db, is_blacklisted_token_set
        try:
            return is_blacklisted_token_db(decrypted_token)
            # return is_blacklist_token_set(decrypted_token)
        except Exception as e:
            app.logger.error(e)
            return make_response(jsonify({'msg': 'session already expired'}, 409))


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
