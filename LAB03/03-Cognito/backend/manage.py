"""
    manage.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    CLI tool for manage application.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import sys
import hmac
import boto3
import base64
import hashlib
import unittest
from flask.cli import FlaskGroup
from cloudalbum import create_app
from cloudalbum.tests.base import user
from cloudalbum.database import delete_table


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
    # Create test user
    msg = '{0}{1}'.format(user['email'], app.config['COGNITO_CLIENT_ID'])
    dig = hmac.new(app.config['COGNITO_CLIENT_SECRET'].encode('utf-8'),
                   msg=msg.encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    try:
        cognito_client = boto3.client('cognito-idp')
        response = cognito_client.sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            SecretHash=base64.b64encode(dig).decode(),
            Username=user['email'],
            Password=user['password'],
            UserAttributes=[{
                'Name': 'name',
                'Value': user['username']
            }],
            ValidationData=[{
                'Name': 'name',
                'Value': user['username']
            }]
        )
        username = response['UserSub']
        cognito_client.admin_confirm_sign_up(
            UserPoolId=app.config['COGNITO_POOL_ID'],
            Username=username
        )
    except cognito_client.exceptions.UsernameExistsException as e:
        pass


if __name__ == '__main__':
    cli()
