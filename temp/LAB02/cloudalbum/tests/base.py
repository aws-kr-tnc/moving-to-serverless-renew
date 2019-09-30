"""
    cloudalbum/tests/base.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Base test cases

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from cloudalbum import create_app, db
from cloudalbum.database.models import User

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
        db.create_all()
        # Create test user
        test_user = User(username=user['username'],
                         email=user['email'], password=generate_password_hash(user['password']))
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


