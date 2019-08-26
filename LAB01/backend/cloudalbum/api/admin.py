from flask import Blueprint
from flask import current_app as app
from flask_restplus import Api, Resource
from cloudalbum.util.response import m_response
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
        return m_response(True, {'msg':'pong!'}, 200)


@api.route('/health_check')
class HealthCheck(Resource):
    @api.doc(responses={200: 'system alive!'})
    def get(self):
        status = True
        try:
            # DB health
            res = db.engine.execute('SELECT 1')
            if res is None:
                app.logger.debug("db not answered!")
                status = False

            # Disk health
            total, used, free = shutil.disk_usage("/")

            if used / total * 100 >= 90:
                app.logger.debug("free disk size under 10%")
                status = False

            #health check result
            if status is False:
                return m_response(False, {'msg':'healthcheck failed'},500)

            app.logger.debug("success:db alive!")
            app.logger.debug("success:health check!")
            return m_response(True, {'msg':'health_check success'}, 200)
        except Exception as e:
            app.logger.error(e)
            app.logger.error("db not answerd")
            return m_response(False, {'msg': 'healthcheck failed'}, 500)
