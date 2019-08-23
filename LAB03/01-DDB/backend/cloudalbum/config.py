
import os

# - FLASK_ENV=production
# - APP_SETTINGS=cloudalbum.config.ProductionConfig
# - DATABASE_URL=postgres://postgres:postgres@users-database:5432/users_prod
# - DATABASE_TEST_URL=postgres://postgres:postgres@users-database:5432/users_test

class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_secret'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')



class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
