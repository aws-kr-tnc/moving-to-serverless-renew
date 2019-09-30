"""
    cloudalbum/tests/test_s3.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test S3 bucket is available.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import unittest
import boto3
import botocore
from cloudalbum.tests.base import BaseTestCase
from flask import current_app as app


class TestS3Service(BaseTestCase):
    """Test S3 Service."""

    def test_bucket_availability(self):
        """Ensure the DDB User table is available."""
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(app.config['S3_PHOTO_BUCKET'])
        exists = True
        try:
            s3.meta.client.head_bucket(Bucket=app.config['S3_PHOTO_BUCKET'])
            self.assertEqual(exists, True)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
                self.assertEqual(exists, True, msg='Bucket is not exist!')


if __name__ == '__main__':
    unittest.main()
