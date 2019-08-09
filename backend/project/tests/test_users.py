
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
        resp = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', resp['data']['msg'])

    def test_user_signup(self):
        """Ensure a new user signup resource."""

        response, new_user = auto_signup(self)
        resp = response.json

        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_user['email'], resp['data']['email'])
        self.assertEqual(new_user['username'], resp['data']['username'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""

        with self.client:
            response = self.client.post(
                '/users/signup',
                data=json.dumps({}),
                content_type='application/json',
            )

            resp = response.json

            self.assertEqual({}, resp['data'])
            self.assertEqual(400, response.status_code)


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
            self.assertIn('super@mario.com', data['data']['email'])


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
            self.assertIn(test_user, duplicated_resp['data'])


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
