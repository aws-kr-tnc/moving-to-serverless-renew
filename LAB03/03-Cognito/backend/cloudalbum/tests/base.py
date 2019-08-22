# services/users/project/tests/base.py


from flask_testing import TestCase

from cloudalbum import create_app

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

