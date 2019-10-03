"""
    cloudalbum/tests/test_photos.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for photos REST API

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import boto3
import pytest
import unittest
import base64
from app import app
from chalice.config import Config
from chalice.local import LocalGateway
from tests.base import BaseTestCase, user as existed_user
from tests.multipart import MultipartFormdataEncoder
from chalicelib import cognito
from chalicelib.model_ddb import Photo

upload = dict(
    tags='ITA, Venezia, SONY , DSLR-A300, 2048 x 1371',
    filename_orig='test_image.jpg',
    desc='TEST',
    make='SONY',
    model='DSLR-A300',
    width='2048',
    height='1371',
    geotag_lat='45.43472222222222',
    geotag_lng='12.346736111111111',
    taken_date='2012:07:15 09:46:46',
    city='Venezia',
    nation='ITA',
    address='Badoer Gritti, Campo Bandiera e Moro o de la Bragora 3608, 30122, Venezia, ITA',
)


class TestPhotoService(BaseTestCase):
    """Tests for the Photo Service."""

    @pytest.fixture(autouse=True)
    def gateway_factory(self):
        config = Config()
        self.gateway = LocalGateway(app, config)

    @pytest.fixture(autouse=True)
    def create_token_and_header(self):
        try:
            client = boto3.client('cognito-idp')
            dig = cognito.generate_digest(existed_user)
            cognito.signup(client, existed_user, dig)
            auth = cognito.generate_auth(existed_user)
            body = cognito.generate_token(client, auth, existed_user)
            self.access_token = body['accessToken']
        except client.exceptions.UsernameExistsException as e:
            # Do nothing
            pass
        finally:
            auth = cognito.generate_auth(existed_user)
            body = cognito.generate_token(client, auth, existed_user)
            self.access_token = body['accessToken']

    @pytest.fixture(autouse=True)
    def multipart_encode(self):
        with open('test_image.jpg', 'rb') as file:
            base64_image = base64.b64encode(file.read())
            upload['base64_image'] = base64_image
            fields = [(k, v) for k, v in upload.items()]
            files = [('file', 'test_image.jpg', file)]
            self.multipart_content_type, self.multipart_body = MultipartFormdataEncoder().encode(fields, files)

    def test_list(self):
        """Ensure the /photos/ route behaves correctly."""
        response = self.gateway.handle_request(
            method='GET',
            path='/photos/',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer {0}'.format(self.access_token)},
            body=None)
        self.assertEqual(response['statusCode'], 200)

    def test_upload(self):
        """Ensure the /photos/file behaves correctly."""
        response = self.gateway.handle_request(
            method='POST',
            path='/photos/file',
            headers={'Content-Type': self.multipart_content_type,
                     'Authorization': 'Bearer {0}'.format(self.access_token)},
            body=self.multipart_body)
        self.assertEqual(response['statusCode'], 200)

    def test_delete(self):
        """Ensure the /photos/<photo_id> route behaves correctly."""
        # 1. upload
        response = self.gateway.handle_request(
            method='POST',
            path='/photos/file',
            headers={'Content-Type': self.multipart_content_type,
                     'Authorization': 'Bearer {0}'.format(self.access_token)},
            body=self.multipart_body)
        self.assertEqual(response['statusCode'], 200)
        photo_id = [item.id for item in Photo.scan(Photo.filename_orig.startswith('test_image.jpg'), limit=1)]
        # 2. delete
        response = self.gateway.handle_request(
            method='DELETE',
            path='/photos/{}'.format(photo_id[0]),
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer {0}'.format(self.access_token)},
            body=None)
        self.assertEqual(response['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()
