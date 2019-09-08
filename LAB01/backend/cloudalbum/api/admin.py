import socket

from flask import Blueprint, make_response
from flask import current_app as app
from flask_restplus import Api, Resource
from werkzeug.exceptions import InternalServerError
from cloudalbum import db
import shutil

admin_blueprint = Blueprint('admin', __name__)
api = Api(admin_blueprint, doc='/swagger/', title='Admin',
          description='CloudAlbum-admin: \n prefix url "/admin" is already exist.', version='0.1')


@api.route('/ping')
class Ping(Resource):
    @api.doc(responses={200: 'pong!'})
    def get(self):
        """Ping api"""
        app.logger.debug("success:ping pong!")
        return make_response({'ok': True, 'Message': 'pong'}, 200)


@api.route('/health_check')
class HealthCheck(Resource):
    @api.doc(responses={200: 'system alive!'})
    def get(self):
        try:
            # 1. Is DB is responsive?!
            db.engine.execute('SELECT 1')
            # 2. Is disk have enough free space?!
            total, used, free = shutil.disk_usage("/")
            if used / total * 100 >= 90:
                raise Exception("free disk size under 10%")
            # 3. Something else..
            # TODO: health check something
            return make_response({'ok': True, 'Message': 'Healthcheck success: {0}'.format(get_ip_addr())}, 200)
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError('Healthcheck failed: {0}: {1}'.format(get_ip_addr(), e))


def get_ip_addr():
    return '{0}'.format(socket.gethostname())
