import json
import pytest
from app import app
from unittest import TestCase
from chalice.config import Config
from chalice.local import LocalGateway


class TestChalice(TestCase):

    @pytest.fixture(autouse=True)
    def gateway_factory(self):
        config = Config()
        self.local_gateway = LocalGateway(app, config)

    def test_ping(self):
        gateway = self.local_gateway
        response = gateway.handle_request(method='GET',
                                          path='/ping',
                                          headers={},
                                          body='')
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), dict([('Message', 'pong'), ('ok', 'true')]))
