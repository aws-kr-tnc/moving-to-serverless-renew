"""
    cloudalbum/tests/test_admin.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Test cases for admin REST API

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import unittest
from cloudalbum.tests.base import BaseTestCase


class TestAdminService(BaseTestCase):
    """Tests for the Photo Service."""

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/admin/ping')
        self.assert200(response, 'pong failed?')

    def test_healthcheck(self):
        """Ensure the /healthcheck route behaves correctly."""
        response = self.client.get('/admin/health_check')
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()
