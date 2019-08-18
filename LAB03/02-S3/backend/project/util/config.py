import os

conf = {
    'UPLOAD_DIR' : '/tmp',
    'AWS_REGION' : 'ap-northeast-2',
    'DDB_RCU' : 2,
    'DDB_WCU' :1,
    'S3_PHOTO_BUCKET': os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-123')
}