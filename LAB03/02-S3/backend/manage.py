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
from cloudalbum import create_app
from cloudalbum.database import delete_table
from cloudalbum.database.model_ddb import User
from werkzeug.security import generate_password_hash

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('delete_db')
def delete_db():
    delete_table()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('cloudalbum/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    try:
        user = User('test_user_id')
        user.email = 'user@user.com'
        user.password = generate_password_hash('Password1!')
        user.username = 'user'
        user.save()
    except Exception as e:
        app.logger.error(e)


if __name__ == '__main__':
    cli()
