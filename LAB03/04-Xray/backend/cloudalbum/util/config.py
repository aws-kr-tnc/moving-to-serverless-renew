import os

conf = {
    'UPLOAD_DIR' : '/tmp',
    'THUMBNAIL_WIDTH': os.getenv('THUMBNAIL_WIDTH', 300),
    'THUMBNAIL_HEIGHT': os.getenv('THUMBNAIL_HEIGHT', 200),

    #DynamoDB
    'AWS_REGION' : os.getenv('AWS_REGION', 'ap-northeast-2'),
    'DDB_RCU' : 2,
    'DDB_WCU' :1,

    #S3
    'S3_PHOTO_BUCKET': os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-123k'),
    'S3_PRESIGNED_URL_EXPIRE_TIME': os.getenv('S3_PRESIGNED_URL_EXPIRE_TIME', 300),

    # COGNITO
    'COGNITO_POOL_ID': os.getenv('COGNITO_POOL_ID', 'ap-northeast-2_1ZYNsRQKc'),
    'COGNITO_CLIENT_ID': os.getenv('COGNITO_CLIENT_ID', '3euucaib97ui39pdtu1e18spaa'),
    'COGNITO_CLIENT_SECRET': os.getenv('COGNITO_CLIENT_SECRET', '1hg3jnk19cf0svnt2jkk1tr0gj6gj7is9sh1sekultgfhnh6i4qj'),
    'COGNITO_DOMAIN': os.getenv('COGNITO_DOMAIN', 'cloudalbum-123k.auth.ap-northeast-2.amazoncognito.com'),
    'BASE_URL': os.getenv('BASE_URL', 'localhost:5000')
}