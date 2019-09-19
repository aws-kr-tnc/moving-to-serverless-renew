"""
    cloudalbum/tests/base.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Base test cases

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
from flask_testing import TestCase
from cloudalbum import create_app
from cloudalbum.database.model_ddb import User
from werkzeug.security import generate_password_hash
import uuid

user = {
    'username': 'test001',
    'email': 'test001@testuser.com',
    'password': 'Password!'
}

app = create_app()


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('cloudalbum.config.TestingConfig')
        return app

    def setUp(self):
        # Insert test user
        test_user = User(uuid.uuid4().hex)
        test_user.email = user['email']
        test_user.username = user['username']
        test_user.password = generate_password_hash(user['password'])
        test_user.save()

    def tearDown(self):
        # Delete test data
        for item in User.scan(User.username.startswith('test')):
            item.delete()
