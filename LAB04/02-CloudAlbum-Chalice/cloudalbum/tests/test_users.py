"""
    cloudalbum/tests/test_users.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for users REST API

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import json
import boto3
import pytest
import unittest
from app import app
from chalice.config import Config
from chalice.local import LocalGateway
from tests.base import BaseTestCase, user as existed_user
from chalicelib import cognito

new_user = {
    'username': 'test002',
    'email': 'test002@testuser.com',
    'password': 'Password1!'
}

bad_user = {
    'username': 'test001',
    'email': 'bad_email',
    'password': 'aa'
}


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    @pytest.fixture(autouse=True)
    def gateway_factory(self):
        config = Config()
        self.gateway = LocalGateway(app, config)

    def test_signup(self):
        """Ensure a new user signup resource."""
        response = self.gateway.handle_request(
            method='POST',
            path='/users/signup',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(new_user))
        self.assertEqual(response['statusCode'], 201)

    def test_bad_signup(self):
        """Check error handling for bad request."""
        response = self.gateway.handle_request(
            method='POST',
            path='/users/signup',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(bad_user))
        self.assertEqual(response['statusCode'], 400)

    def test_signup_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        response = self.gateway.handle_request(
            method='POST',
            path='/users/signup',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(existed_user))
        self.assertEqual(response['statusCode'], 409)

    def test_signin(self):
        """Ensure signin request works well."""
        response = self.gateway.handle_request(
            method='POST',
            path='/users/signin',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(existed_user))
        self.assertEqual(response['statusCode'], 200)
        self.assertNotEqual(json.loads(response['body'])['accessToken'], None)

    def test_bad_signin(self):
        """Check error handling for bad request."""
        response = self.gateway.handle_request(
            method='POST',
            path='/users/signin',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(bad_user))
        self.assertEqual(response['statusCode'], 400)

    def test_signout(self):
        """Ensure signout request works well."""
        client = boto3.client('cognito-idp')
        auth = cognito.generate_auth(existed_user)
        body = cognito.generate_token(client, auth, existed_user)
        response = self.gateway.handle_request(
            method='POST',
            path='/users/signout',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer {0}'.format(body['accessToken'])},
            body=json.dumps(bad_user))
        self.assertEqual(response['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()
