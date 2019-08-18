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
    'S3_PRESIGNED_URL_EXPIRE_TIME': os.getenv('S3_PRESIGNED_URL_EXPIRE_TIME', 30),

    # COGNITO
    'COGNITO_POOL_ID': os.getenv('COGNITO_POOL_ID', '<YOUR_POOL_ID>'),
    'COGNITO_CLIENT_ID': os.getenv('COGNITO_CLIENT_ID', '<YOUR_CLIENT_ID>'),
    'COGNITO_CLIENT_SECRET': os.getenv('COGNITO_CLIENT_SECRET', '<YOUR_CLIENT_SECRET>'),
    'COGNITO_DOMAIN': os.getenv('COGNITO_DOMAIN', '<YOUR_COGNITO_DOMAIN>'),
    'BASE_URL': os.getenv('BASE_URL', '<PREVIEW_URL>')
}