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
from aws_xray_sdk.core import xray_recorder, patch_all, patch
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from bson.objectid import ObjectId
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from cloudalbum.database import create_table


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

    # instantiate the app
    app = Flask(__name__)

    flask_bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    app.json_encoder = JSONEncoder

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # TODO 9: Review X-ray setting
    patch_modules = (
        'boto3',
        'botocore',
        'pynamodb',
        'requests',
    )
    plugins = ('EC2Plugin',)
    xray_recorder.configure(service='CloudAlbum',
                            plugins=plugins,
                            context_missing='LOG_ERROR',
                            sampling=False)
    xray_recorder.begin_segment('cloudalbum')
    XRayMiddleware(app, xray_recorder)
    patch(patch_modules)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set logger to STDOUT
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.DEBUG)

    # Create database table, if it is not exists
    with app.app_context():
        create_table()

    # register blueprints
    from cloudalbum.api.users import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from cloudalbum.api.photos import photos_blueprint
    app.register_blueprint(photos_blueprint, url_prefix='/photos')

    from cloudalbum.api.admin import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}
    return app
