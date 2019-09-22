"""
    cloudalbum/tests/test_photos.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for photos REST API

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import pytest
import unittest
from io import BytesIO
from cloudalbum.tests.base import BaseTestCase
from cloudalbum.database.model_ddb import Photo
from flask_jwt_extended import create_access_token

for_user_token = {
    'user_id': 'test001',
    'email': 'test001@testuser.com',
    'password': 'Password1!'
}


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
    address='Badoer Gritti, Campo Bandiera e Moro o de la Bragora 3608, 30122, Venezia, ITA'
)


class TestPhotoService(BaseTestCase):
    """Tests for the Photo Service."""

    @pytest.fixture(autouse=True)
    def create_token_and_header(self):
        with self.app.app_context():
            self.access_token = create_access_token(identity=for_user_token)
            self.test_header = dict(Authorization='Bearer {0}'.format(self.access_token))

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get(
            '/photos/ping',
            headers=self.test_header,
            content_type='application/json',
        )
        self.assert200(response)

    def test_upload(self):
        """Ensure the /photos/file behaves correctly."""
        upload['file'] = (BytesIO(b'my file contents'), 'test_image.jpg')
        response = self.client.post(
            '/photos/file',
            headers=self.test_header,
            content_type='multipart/form-data',
            data=upload
        )
        self.assert200(response)

    def test_list(self):
        """Ensure the /photos/ route behaves correctly."""
        access_token = create_access_token(identity=for_user_token)
        response = self.client.get(
            '/photos/',
            headers=self.test_header,
            content_type='application/json',
        )
        self.assert200(response)

    def test_delete(self):
        """Ensure the /photos/<photo_id> route behaves correctly."""
        access_token = create_access_token(identity=for_user_token)
        # 1. upload
        upload['file'] = (BytesIO(b'my file contents'), 'test_image.jpg')
        response = self.client.post(
            '/photos/file',
            headers=self.test_header,
            content_type='multipart/form-data',
            data=upload
        )
        self.assert200(response)
        photo_id = None
        for item in Photo.scan(Photo.filename_orig.startswith('test_image.jpg'), limit=1):
            photo_id = item.id
        # 2. delete
        response = self.client.delete(
            '/photos/{}'.format(photo_id),
            headers=self.test_header,
            content_type='application/json',
        )
        self.assert200(response)

    def test_get_mode_thumb_orig(self):
        """Ensure the /photos/<photo_id>?mode=thumbnail route behaves correctly."""
        access_token = create_access_token(identity=for_user_token)
        # 1. upload
        upload['file'] = (BytesIO(b'my file contents'), 'test_image.jpg')
        response = self.client.post(
            '/photos/file',
            headers=self.test_header,
            content_type='multipart/form-data',
            data=upload
        )
        self.assert200(response)
        photo_id = None
        for item in Photo.scan(Photo.filename_orig.startswith('test_image.jpg'), limit=1):
            photo_id = item.id
        # 2. thumbnails
        data = {'mode': 'thumbnails'}
        response = self.client.get(
            '/photos/{}'.format(photo_id),
            headers=self.test_header,
            content_type='application/json',
            query_string=data
        )
        self.assert200(response)
        # 3. original
        data = {'mode': 'original'}
        response = self.client.get(
            '/photos/{}'.format(photo_id),
            headers=self.test_header,
            content_type='application/json',
            query_string=data
        )
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()
