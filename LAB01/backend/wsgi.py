"""
    wsgi.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    WSGI(Web Server Gateway Interface) script to deploy AWS ElasticBeanstalk.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""

import os
from cloudalbum import create_app, db

application = create_app()

application.logger.info('SQLALCHEMY_DATABASE_URI: {0}'.format(application.config['SQLALCHEMY_DATABASE_URI']))
application.logger.info('UPLOAD_FOLDER: {0}'.format(application.config['UPLOAD_FOLDER']))

APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
APP_PORT = os.getenv('APP_PORT', 8080)

if __name__ == '__main__':
    application.run(host=APP_HOST, port=APP_PORT)
