"""
    cloudalbum/solution.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Hands-on lab solution file.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import boto3
import base64
from datetime import datetime
from flask import current_app as app
from werkzeug.exceptions import Unauthorized
from cloudalbum.database.model_ddb import Photo


def solution_put_photo_info_ddb(user_id, filename, form, filesize):
    new_photo = Photo(id=filename,
                      user_id=user_id,
                      filename=filename,
                      filename_orig=form['file'].filename,
                      filesize=filesize,
                      upload_date=datetime.today(),
                      tags=form['tags'],
                      desc=form['desc'],
                      geotag_lat=form['geotag_lat'],
                      geotag_lng=form['geotag_lng'],
                      taken_date=datetime.strptime(form['taken_date'], "%Y:%m:%d %H:%M:%S"),
                      make=form['make'],
                      model=form['model'],
                      width=form['width'],
                      height=form['height'],
                      city=form['city'],
                      nation=form['nation'],
                      address=form['address'])
    new_photo.save()


def solution_put_object_to_s3(s3_client, key, upload_file_stream):
    s3_client.put_object(
        Bucket=app.config['S3_PHOTO_BUCKET'],
        Key=key,
        Body=upload_file_stream,
        ContentType='image/jpeg',
        StorageClass='STANDARD'
    )
    app.logger.debug('success:put object into s3:key:{}'.format(key))


def solution_generate_s3_presigned_url(s3_client, key):
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': app.config['S3_PHOTO_BUCKET'],
                'Key': key})
    return url


def user_signup_confirm(id):
    client = boto3.client('cognito-idp')
    client.admin_confirm_sign_up(
        UserPoolId=app.config['COGNITO_POOL_ID'],
        Username=id
    )
    app.logger.debug('success: user confirm automatically:user id:{}'.format(id))


def solution_signup_cognito(user, dig):
    app.logger.info('RUNNING TODO#7 SOLUTION CODE:')
    app.logger.info('Enroll user into Cognito!')
    app.logger.info('Follow the steps in the lab guide to replace this method with your own implementation.')

    client = boto3.client('cognito-idp')
    response = client.sign_up(
        ClientId=app.config['COGNITO_CLIENT_ID'],
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


def solution_get_cognito_user_data(access_token):
    app.logger.info('RUNNING TODO#8 SOLUTION CODE:')
    app.logger.info('Get user data from Cognito!')
    app.logger.info('Follow the steps in the lab guide to replace this method with your own implementation.')
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
        raise Unauthorized('Invalid Access Token')
