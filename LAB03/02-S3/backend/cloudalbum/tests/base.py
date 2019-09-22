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
from cloudalbum.database.model_ddb import User, Photo
from werkzeug.security import generate_password_hash
import uuid

user = {
    'username': 'test001',
    'email': 'test001@testuser.com',
    'password': 'Password1!'
}


class BaseTestCase(TestCase):
    app = create_app()

    def create_app(self):
        self.app.config.from_object('cloudalbum.config.TestingConfig')
        return self.app

    def setUp(self):
        # Delete any test data that may be remained.
        for item in Photo.scan(Photo.filename_orig.startswith('test')):
            item.delete()
        # Create test user
        test_user = User(uuid.uuid4().hex)
        test_user.email = user['email']
        test_user.username = user['username']
        test_user.password = generate_password_hash(user['password'])
        test_user.save()

    def tearDown(self):
        # Delete test data
        for item in User.scan(User.username.startswith('test')):
            item.delete()
        for item in Photo.scan(Photo.filename_orig.startswith('test')):
            item.delete()
