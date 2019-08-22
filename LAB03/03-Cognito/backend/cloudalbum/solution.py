import base64

import boto3
from flask import current_app as app
from werkzeug.security import generate_password_hash

from cloudalbum.database.model_ddb import User
from cloudalbum.util.config import conf


def solution_put_new_user(new_user_id, user_data):
    user = User(new_user_id)
    user.email = user_data['email']
    user.password = generate_password_hash(user_data['password'])
    user.username = user_data['username']
    user.photos = []
    user.save()



def solution_get_user_data_with_idx(signin_data):
    db_user = None
    for item in User.email_index.query(signin_data['email']):
        if item is not None:
            db_user = item
    return db_user

def solution_put_photo_info_ddb(user_id, new_photo):
    try:
        User(id=user_id).update(
            actions=[
                User.photos.set((User.photos | []).append([new_photo]))
            ]
        )
        app.logger.debug('success:create photo into ddb: user_id:{}, photo_id:{}'.format(user_id, new_photo.id))
    except Exception as e:

        app.logger.error(e)
        raise e


def solution_delete_photo_from_ddb(user, photos, photo):
    try:
        photos.remove(photo)
        User(id=user['user_id']).update(
            actions=[
                User.photos.set(photos)
            ]
        )
        app.logger.debug("success:delete photo from ddb: userid:{}, photo_id:{}".format(user['user_id'], photo.id))
    except Exception as e:
        app.logger.error("ERROR:delete photo from ddb failed: userid:{}, photo_id:{}".format(user['user_id'], photo.id))
        app.logger.error(e)
        raise e

def solution_put_object_to_s3(s3_client, key, upload_file_stream):
    try:
        s3_client.put_object(
            Bucket=conf['S3_PHOTO_BUCKET'],
            Key=key,
            Body=upload_file_stream,
            ContentType='image/jpeg',
            StorageClass='STANDARD'
        )
        app.logger.debug('success:put object into s3:key:{}'.format(key))

    except Exception as e:
        app.logger.error('ERROR:failed put object: key:{}'.format(key))
        app.logger.error(e)
        raise e


def solution_generate_s3_presigned_url(s3_client, key):
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': conf['S3_PHOTO_BUCKET'],
                'Key': key})
    return url


def user_signup_confirm(id):
    client = boto3.client('cognito-idp')
    try:
        client.admin_confirm_sign_up(
            UserPoolId=conf['COGNITO_POOL_ID'],
            Username=id
        )
        app.logger.debug('success: user confirm automatically:user id:{}'.format(id))
    except Exception as e:
        app.logger.error('ERROR: user confirm failed:user id:{}'.format(id))
        app.logger.error(e)


def solution_signup_cognito(user, dig):
    app.logger.info("RUNNING TODO#7 SOLUTION CODE:")
    app.logger.info("Enroll user into Cognito!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    client = boto3.client('cognito-idp')
    try:
        response = client.sign_up(
            ClientId=conf['COGNITO_CLIENT_ID'],
            SecretHash=base64.b64encode(dig).decode(),
            Username=user['email'],
            Password=user['password'],
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': user['username']
                }
            ],
            ValidationData=[
                {
                    'Name': 'name',
                    'Value': user['username']
                }
            ]

        )

        email = response['CodeDeliveryDetails']['Destination']
        id = response['UserSub']

        # automatically confirm user for lab
        user_signup_confirm(id)
        return {'email': email, 'id': id}
    except Exception as e:
        app.logger.error('ERROR:failed to enroll user into cognito')
        app.logger.error(e)


def solution_get_cognito_user_data(access_token):
    app.logger.info("RUNNING TODO#8 SOLUTION CODE:")
    app.logger.info("Get user data from Cognito!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation." )
    client = boto3.client('cognito-idp')
    try:
        cognito_user = client.get_user(AccessToken=access_token)

        user_data = {}
        for attr in cognito_user['UserAttributes']:
            key = attr['Name']
            if key == 'sub':
                key = 'user_id'
            val = attr['Value']
            user_data[key] = val
        app.logger.debug('success: get Cognito user data: {}'.format(user_data))
        return user_data
    except Exception as e:
        app.logger.error('ERROR: failed to get Cognito user data:access token: {}'.format(access_token))