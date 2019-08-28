import datetime
import os

class BaseConfig:
    """Base configuration"""

    TESTING = False
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = os.getenv('APP_PORT', 8080)

    SECRET_KEY = os.getenv('FLASK_SECRET', os.urandom(24))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'my_jwt')
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', datetime.timedelta(days=1))
    JWT_BLACKLIST_ENABLED = os.getenv('JWT_BLACKLIST_ENABLED', True)
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'upload'))
    THUMBNAIL_WIDTH = os.getenv('THUMBNAIL_WIDTH', 300)
    THUMBNAIL_HEIGHT = os.getenv('THUMBNAIL_HEIGHT', 200)

    AWS_REGION = os.getenv('AWS_REGION', 'ap-southeast-1')

    # DynamoDB
    DDB_RCU = os.getenv('DDB_RCU', 10)
    DDB_WCU = os.getenv('DDB_WCU', 10)

    # S3
    S3_PHOTO_BUCKET = os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-<your-initial>')
    S3_PRESIGNED_URL_EXPIRE_TIME = os.getenv('S3_PRESIGNED_URL_EXPIRE_TIME', 3600)

    # Cognito
    COGNITO_POOL_ID = os.getenv('COGNITO_POOL_ID', '<input-your-cognito-pool-id>'),
    COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID', '<input-your-cognito-client-id>'),
    COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET', '<input-your-cognito-client-secret>'),
    COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN', '<input-your-cognito-domain>'),


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
