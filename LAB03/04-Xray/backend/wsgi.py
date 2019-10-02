"""
    wsgi.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    WSGI(Web Server Gateway Interface) script to deploy AWS ElasticBeanstalk.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""

import os
from cloudalbum import create_app

application = create_app()

APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
APP_PORT = os.getenv('APP_PORT', 8080)

if __name__ == '__main__':
    application.run(host=APP_HOST, port=APP_PORT)
