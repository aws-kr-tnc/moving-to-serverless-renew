import os

conf = {
    'UPLOAD_DIR' : '/tmp',
    'AWS_REGION' : os.getenv('AWS_REGION', 'ap-northeast-2'),
    'DDB_RCU' : 2,
    'DDB_WCU' :1,
    'S3_PHOTO_BUCKET': os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-123k'),
    'THUMBNAIL_WIDTH': os.getenv('THUMBNAIL_WIDTH', 300),
    'THUMBNAIL_HEIGHT': os.getenv('THUMBNAIL_HEIGHT', 200),
    'S3_PRESIGNED_URL_EXPIRE_TIME': os.getenv('S3_PRESIGNED_URL_EXPIRE_TIME', 30)

}