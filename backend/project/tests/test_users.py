
import json
import unittest
import random

from project.tests.base import BaseTestCase

def auto_signup(self):
    """Signup tool for test user """
    random_int = random.randint(0, 1000000)
    dic_user = {
        "username": "user" + str(random_int),
        "email":"%s@mario.com" % random_int,
        'password': '%s_password' % random_int
    }

    with self.client:
        response = self.client.post(
            '/users/signup',
            data=json.dumps(dic_user),
            content_type='application/json',
        )
        return response, dic_user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, data['code'])
        self.assertIn('pong!', data['message'])

    def test_user_signup(self):
        """Ensure a new user signup resource."""

        response, new_user = auto_signup(self)
        response_json = response.json

        self.assertEqual(response.status_code, 201)
        self.assertEqual(201, response_json['code'])
        self.assertIn('Signup Success!', response_json['message'])
        self.assertEqual(new_user['email'], response_json['data']['user']['email'])
        self.assertEqual(new_user['username'], response_json['data']['user']['username'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""

        with self.client:
            response = self.client.post(
                '/users/signup',
                data=json.dumps({}),
                content_type='application/json',
            )

            data = response.json

            self.assertEqual(response.status_code, 400)
            self.assertEqual(400, data['code'])
            self.assertIn('Bad request', data['message'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
                '/users/signup',
                data=json.dumps({'email': 'super@mario.com'}),
                content_type='application/json',
            )
            data = response.json

            self.assertEqual(response.status_code, 400)
            self.assertEqual(400, data['code'])
            self.assertIn('Bad request', data['message'])


    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        response, test_user = auto_signup(self)

        if response.status_code is 201:
            with self.client:
                second_response = self.client.post(
                    '/users/signup',
                    data=json.dumps(test_user),
                    content_type='application/json'
                )
            duplicated_resp = second_response.json
            self.assertEqual(second_response.status_code, 400)
            self.assertEqual(400, duplicated_resp['code'])
            self.assertIn('Sorry. This email already exists.', duplicated_resp['message'])


    def test_single_user_search(self):
        """Ensure get single user behaves correctly."""

        response, test_user = auto_signup(self)
        result = response.json

        with self.client:
            response = self.client.get('/users/%s' % result['data']['user']['id'])
            search_result_user =result['data']['user']

            self.assertEqual(response.status_code, 200)
            self.assertIn(test_user['username'], search_result_user['username'])
            self.assertIn(test_user['email'], search_result_user['email'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/1000000000000')
            result = response.json
            self.assertEqual(response.status_code, 404)
            self.assertIn('Not exist user id', result['message'])
            self.assertEqual(404, result['code'])


if __name__ == '__main__':
    unittest.main()
