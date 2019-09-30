"""
    cloudalbum/tests/test_config.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for application configuration

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import unittest
from flask import current_app
from flask_testing import TestCase
from cloudalbum import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('cloudalbum.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'dev_secret')
        self.assertFalse(current_app is None)

    def test_ddb_rcu(self):
        self.assertIsNotNone(app.config['DDB_RCU'])

    def test_ddb_wcu(self):
        self.assertIsNotNone(app.config['DDB_WCU'])

    def test_s3_bucket(self):
        self.assertIsNotNone(app.config['S3_PHOTO_BUCKET'])

    def test_cognito_pool_id(self):
        self.assertIsNotNone(app.config['COGNITO_POOL_ID'])

    def test_cognito_client_id(self):
        self.assertIsNotNone(app.config['COGNITO_CLIENT_ID'])

    def test_cognito_client_secret(self):
        self.assertIsNotNone(app.config['COGNITO_CLIENT_SECRET'])


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('cloudalbum.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'test_secret')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])

    def test_ddb_rcu(self):
        self.assertIsNotNone(app.config['DDB_RCU'])

    def test_ddb_wcu(self):
        self.assertIsNotNone(app.config['DDB_WCU'])

    def test_s3_bucket(self):
        self.assertIsNotNone(app.config['S3_PHOTO_BUCKET'])

    def test_cognito_pool_id(self):
        self.assertIsNotNone(app.config['COGNITO_POOL_ID'])

    def test_cognito_client_id(self):
        self.assertIsNotNone(app.config['COGNITO_CLIENT_ID'])

    def test_cognito_client_secret(self):
        self.assertIsNotNone(app.config['COGNITO_CLIENT_SECRET'])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('cloudalbum.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'prod_secret')
        self.assertFalse(app.config['TESTING'])

    def test_ddb_rcu(self):
        self.assertIsNotNone(app.config['DDB_RCU'])

    def test_ddb_wcu(self):
        self.assertIsNotNone(app.config['DDB_WCU'])

    def test_s3_bucket(self):
        self.assertIsNotNone(app.config['S3_PHOTO_BUCKET'])

    def test_cognito_pool_id(self):
        self.assertIsNotNone(app.config['COGNITO_POOL_ID'])

    def test_cognito_client_id(self):
        self.assertIsNotNone(app.config['COGNITO_CLIENT_ID'])

    def test_cognito_client_secret(self):
        self.assertIsNotNone(app.config['COGNITO_CLIENT_SECRET'])


if __name__ == '__main__':
    unittest.main()
