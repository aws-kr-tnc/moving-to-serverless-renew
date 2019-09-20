"""
    cloudalbum/tests/test_users.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for users REST API

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import json
import unittest

import boto3
from cloudalbum.api.users import cognito_signin
from cloudalbum.tests.base import BaseTestCase, user as existed_user


new_user = {
    'username': 'test002',
    'email': 'test002@testuser.com',
    'password': 'Password1!'
}

bad_user = {
    'username': 'user001',
    'email': 'bad_email',
    'password': 'aa'
}


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        self.assert200(response, 'pong failed?')

    def test_signup(self):
        """Ensure a new user signup resource."""
        with self.client:
            response = self.client.post(
                '/users/signup', data=json.dumps(new_user), content_type='application/json', )
            self.assertEqual(response.status_code, 201)

    def test_bad_signup(self):
        """Check error handling for bad request."""
        with self.client:
            response = self.client.post(
                '/users/signup', data=json.dumps(bad_user), content_type='application/json', )
            self.assertEqual(response.status_code, 400)

    def test_signin(self):
        """Ensure signin request works well."""
        with self.client:
            response = self.client.post(
                '/users/signin', data=json.dumps(existed_user), content_type='application/json', )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(response.json['accessToken'], None)

    def test_bad_signin(self):
        """Check error handling for bad request."""
        with self.client:
            response = self.client.post(
                '/users/signin', data=json.dumps(bad_user), content_type='application/json', )
            resp = response.json
            self.assertEqual(response.status_code, 400)

    def test_signup_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            response = self.client.post(
                '/users/signup', data=json.dumps(existed_user), content_type='application/json', )
            self.assertEqual(response.status_code, 409)

    def test_signout(self):
        """Ensure signout request works well."""
        with self.client:
            access_token, _ = cognito_signin(boto3.client('cognito-idp'), existed_user)
            # access_token = create_access_token(identity=existed_user)
            # Signout
            response = self.client.post(
                '/users/signout',
                headers=dict(
                    Authorization='Bearer {0}'.format(access_token)
                ),
                content_type='application/json',
            )
            self.assert200(response)


if __name__ == '__main__':
    unittest.main()
