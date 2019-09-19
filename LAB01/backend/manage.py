"""
    manage.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    CLI tool for manage application.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""

import sys
import unittest
from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from cloudalbum import create_app, db
from cloudalbum.database.models import User

user = {
    'username': 'test001',
    'email': 'test001@testuser.com',
    'password': 'Password1!'
}

app = create_app()
cli = FlaskGroup(create_app=create_app)

app.logger.info('SQLALCHEMY_DATABASE_URI: {0}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
app.logger.info('UPLOAD_FOLDER: {0}'.format(app.config['UPLOAD_FOLDER']))


@cli.command('recreate_db')
def recreate_db():
    """
    Re-create database tables.
    :return:
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('test')
def test():
    """
    Runs the tests without code coverage
    :return:
    """
    tests = unittest.TestLoader().discover('cloudalbum/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command('seed_db')
def seed_db():
    """
    Insert seeds database
    :return:
    """
    db.session.add(User(username=user['username'], email=user['email'],
                        password=generate_password_hash(user['password'])))
    db.session.commit()


if __name__ == '__main__':
    cli()
