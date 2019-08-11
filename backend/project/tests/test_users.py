
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

def auto_signin(self, test_user):
    with self.client:
        response = self.client.post(
            '/users/signin',
            data=json.dumps(test_user),
            content_type='application/json',
        )
        return response


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        self.assert200(response, "pong failed?")

    def test_user_signup(self):
        """Ensure a new user signup resource."""

        response, new_user = auto_signup(self)
        resp = response.json

        self.assertEqual(response.status_code, 201)
        del new_user['password']
        del resp['data']['id']
        self.assertEquals(new_user, resp['data'])

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
            self.assert400(response, "response code is not 400")


    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        data_invalid = {'email': 'super@mario.com'}
        with self.client:
            response = self.client.post(
                '/users/signup',
                data=json.dumps(data_invalid),
                content_type='application/json',
            )
            resp = response.json
            self.assert400(response, "response code is not 400")
            self.assertEqual(data_invalid, resp['data'])


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

            self.assertEqual(second_response.status_code, 409)
            self.assertEqual(test_user, duplicated_resp['data'])


    def test_single_user_search(self):
        """Ensure get single user behaves correctly."""

        response, test_user = auto_signup(self)
        result = response.json

        with self.client:
            response = self.client.get('/users/%s' % result['data']['id'])
            search_result_user =result['data']

            del search_result_user['id']
            del test_user['password']

            self.assertEqual(response.status_code, 200)
            self.assertEqual(test_user, search_result_user)


    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/1000000000000')
            self.assert404(response, "not exist user failed")

    def test_signout(self):
        # signup user
        response, test_user = auto_signup(self)

        #signin user -> get jwt token
        del test_user['username']
        signing_resp = auto_signin(self, test_user)
        access_token = signing_resp.get_json()['accessToken']

        # signout with token
        response = self.client.post(
            '/users/signout',
            headers=dict(
                Authorization='Bearer ' + signing_resp.get_json()['accessToken']
            ),
            content_type='application/json',
        )

        self.assert200(response)






if __name__ == '__main__':
    unittest.main()
