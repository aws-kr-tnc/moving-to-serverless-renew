"""
    cloudalbum/tests/test_dynamodb.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test DynamoDB tables are available

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import unittest

import pytest

from cloudalbum.tests.base import BaseTestCase
from cloudalbum.database.model_ddb import Photo


class TestDynamoDBService(BaseTestCase):
    """Test DynamoDB Service."""

    # User table is no more needed
    # def test_user_table(self):
    #     """Ensure the DDB User table is available."""
    #     self.assertEqual(User.exists(), True)

    def test_photo_table(self):
        """Ensure the DDB Photo table is available."""
        self.assertEqual(Photo.exists(), True)


if __name__ == '__main__':
    unittest.main()
