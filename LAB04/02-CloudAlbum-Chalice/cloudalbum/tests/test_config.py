"""
    cloudalbum/tests/test_config.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for application configuration

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import unittest
from unittest import TestCase
from chalicelib.config import conf


class TestConfig(TestCase):

    def test_config(self):
        self.assertIsNotNone(conf)

    def test_ddb_rcu(self):
        self.assertIsNotNone(conf['DDB_RCU'])

    def test_ddb_wcu(self):
        self.assertIsNotNone(conf['DDB_WCU'])

    def test_s3_config(self):
        self.assertIsNotNone(conf['S3_PHOTO_BUCKET'])

    def test_cognito_pool_id(self):
        self.assertIsNotNone(conf['COGNITO_POOL_ID'])

    def test_cognito_client_id(self):
        self.assertIsNotNone(conf['COGNITO_CLIENT_ID'])

    def test_cognito_client_secret(self):
        self.assertIsNotNone(conf['COGNITO_CLIENT_SECRET'])


if __name__ == '__main__':
    unittest.main()
