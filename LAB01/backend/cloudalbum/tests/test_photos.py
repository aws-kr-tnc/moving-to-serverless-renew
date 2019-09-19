"""
    cloudalbum/tests/test_photos.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for photos REST API

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
from io import BytesIO
from cloudalbum.tests.base import BaseTestCase
from flask_jwt_extended import create_access_token

user = {
    'user_id': 'testuser',
    'email': 'testuser@testuser.com',
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


def get_header(access_token):
    headers = dict(Authorization='Bearer {0}'.format(access_token))
    return headers


class TestPhotoService(BaseTestCase):
    """Tests for the Photo Service."""

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        access_token = create_access_token(identity=user)
        response = self.client.get(
            '/photos/ping',
            headers=get_header(access_token),
            content_type='application/json',
        )
        self.assert200(response)

    def test_upload(self):
        """Ensure the /photos/file behaves correctly."""
        access_token = create_access_token(identity=user)
        upload['file'] = (BytesIO(b'my file contents'), 'test_image.jpg')
        response = self.client.post(
            '/photos/file',
            headers=get_header(access_token),
            content_type='multipart/form-data',
            data=upload
        )
        self.assert200(response)

    def test_list(self):
        """Ensure the /photos/ route behaves correctly."""
        access_token = create_access_token(identity=user)
        response = self.client.get(
            '/photos/',
            headers=get_header(access_token),
            content_type='application/json',
        )
        self.assert200(response)

    def test_delete(self):
        """Ensure the /photos/<photo_id> route behaves correctly."""
        access_token = create_access_token(identity=user)
        # 1. upload
        upload['file'] = (BytesIO(b'my file contents'), 'test_image.jpg')
        response = self.client.post(
            '/photos/file',
            headers=get_header(access_token),
            content_type='multipart/form-data',
            data=upload
        )
        self.assert200(response)
        photo_id = response.json['photo_id']
        # 2. delete
        response = self.client.delete(
            '/photos/{}'.format(photo_id),
            headers=get_header(access_token),
            content_type='application/json',
        )
        self.assert200(response)

    def test_get_mode_thumb_orig(self):
        """Ensure the /photos/<photo_id>?mode=thumbnail route behaves correctly."""
        access_token = create_access_token(identity=user)
        # 1. upload
        upload['file'] = (BytesIO(b'my file contents'), 'test_image.jpg')
        response = self.client.post(
            '/photos/file',
            headers=get_header(access_token),
            content_type='multipart/form-data',
            data=upload
        )
        self.assert200(response)
        photo_id = response.json['photo_id']

        # 2. thumbnails
        data = {'mode': 'thumbnails'}
        response = self.client.get(
            '/photos/{}'.format(photo_id),
            headers=get_header(access_token),
            content_type='application/json',
            query_string=data
        )
        self.assert200(response)

        # 3. original
        data = {'mode': 'original'}
        response = self.client.get(
            '/photos/{}'.format(photo_id),
            headers=get_header(access_token),
            content_type='application/json',
            query_string=data
        )
        self.assert200(response)
