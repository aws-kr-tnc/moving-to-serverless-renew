"""
    cloudalbum/api/admin.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    REST API for site administrator.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
from botocore.exceptions import ClientError
from flask import Blueprint, make_response
from flask import current_app as app
from flask_restplus import Api, Resource
from werkzeug.exceptions import InternalServerError
import shutil
import socket
import boto3

admin_blueprint = Blueprint('admin', __name__)
api = Api(admin_blueprint, doc='/swagger/', title='Admin',
          description='CloudAlbum-admin: \n prefix url "/admin" is already exist.', version='0.1')


@api.route('/ping')
class Ping(Resource):
    @api.doc(responses={200: 'pong!'})
    def get(self):
        """Ping api"""
        app.logger.debug('success:ping pong!')
        return make_response({'ok': True, 'Message': 'pong'}, 200)


@api.route('/health_check')
class HealthCheck(Resource):
    @api.doc(responses={200: 'system alive!'})
    def get(self):
        try:
            # 1. Is database available?!
            boto3.client('dynamodb').describe_table(TableName='Photo')
            boto3.client('dynamodb').describe_table(TableName='User')

            # 2. Is disk have enough free space?!
            total, used, free = shutil.disk_usage('/')
            if used / total * 100 >= 90:
                raise Exception('free disk size under 10%')
            # 3. Something else..
            # TODO: health check something

            return make_response({'ok': True, 'Message': 'Healthcheck success: {0}'.format(get_ip_addr())}, 200)
        except ClientError as ce:
            app.logger.error(ce)
            raise InternalServerError('Dynamodb healthcheck failed: hostname: {0}'.format(get_ip_addr()))
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError('Healthcheck failed, hostname:'.format(get_ip_addr()))

def get_ip_addr():
    return '{0}'.format(socket.gethostname())

