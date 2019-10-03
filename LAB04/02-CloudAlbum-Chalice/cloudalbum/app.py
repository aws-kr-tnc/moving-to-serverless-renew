"""
    cloudalbum/app.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    AWS Chalice main application module

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""

import uuid
import json
import boto3
import base64
import logging
from chalicelib import cognito
from chalicelib.config import cors_config
from chalicelib.util import pp, save_s3_chalice, get_parts, delete_s3
from chalicelib.model_ddb import Photo, create_photo_info, ModelEncoder, with_presigned_url
from chalice import Chalice, Response, ConflictError, BadRequestError, AuthResponse, ChaliceViewError
from botocore.exceptions import ParamValidationError

app = Chalice(app_name='cloudalbum')
app.debug = True
app.log.setLevel(logging.DEBUG)


@app.authorizer()
def jwt_auth(auth_request):
    """
    JWT based authorizer
    :param auth_request:
    :return: AuthResponse
    """
    token = auth_request.token
    try:
        decoded = cognito.token_decoder(token)
        return AuthResponse(routes=['*'], principal_id=decoded['sub'])
    except Exception as e:
        app.log.error(e)
        return AuthResponse(routes=[''], principal_id='')


@app.route('/photos', methods=['GET'], cors=cors_config,
           authorizer=jwt_auth, content_types=['application/json'])
def photo_list():
    """
    Retrieve Photo table items with signed URL attribute.
    :return:
    """
    current_user = cognito.user_info(cognito.get_token(app.current_request))
    try:
        photos = Photo.query(current_user['user_id'])
        data = {'ok': True, 'photos': []}
        [data['photos'].append(with_presigned_url(current_user, photo)) for photo in photos]
        body = json.dumps(data, cls=ModelEncoder)
        return Response(status_code=200, body=body,
                        headers={'Content-Type': 'application/json'})
    except Exception as e:
        raise ChaliceViewError(e)


@app.route('/photos/file', methods=['POST'], cors=cors_config,
           authorizer=jwt_auth, content_types=['multipart/form-data'])
def upload():
    """
    File upload with multipart/form data.
    :return:
    """
    form = get_parts(app)
    filename_orig = form['filename_orig'][0].decode('utf-8')
    extension = (filename_orig.rsplit('.', 1)[1]).lower()
    base64_image = form['base64_image'][0].decode('utf-8').replace('data:image/jpeg;base64,', '')
    imgdata = base64.b64decode(base64_image)

    try:
        current_user = cognito.user_info(cognito.get_token(app.current_request))
        filename = "{0}.{1}".format(uuid.uuid4(), extension)
        filesize = save_s3_chalice(imgdata, filename, current_user['email'], app.log)
        new_photo = create_photo_info(current_user['user_id'], filename, filesize, form)
        new_photo.save()
        return Response(status_code=200, body={'ok': True},
                        headers={'Content-Type': 'application/json'})
    except Exception as e:
        raise ChaliceViewError(e)


@app.route('/photos/{photo_id}', methods=['DELETE'], cors=cors_config,
           authorizer=jwt_auth, content_types=['application/json'])
def delete(photo_id):
    """
    Delete specific item in Photo table and S3 object
    :param photo_id:
    :return:
    """
    current_user = cognito.user_info(cognito.get_token(app.current_request))
    try:
        photo = Photo.get(current_user['user_id'], photo_id)
        file_deleted = delete_s3(app.log, photo.filename, current_user)
        photo.delete()
        body = data = {'ok': True, 'photo_id': photo_id}
        return Response(status_code=200, body=body,
                        headers={'Content-Type': 'application/json'})
    except Exception as e:
        raise ChaliceViewError(e)


@app.route('/users/signin', methods=['POST'],
           cors=cors_config, content_types=['application/json'])
def signin():
    """
    Sign in to retrieve JWT.
    :return:
    """
    req_data = app.current_request.json_body
    auth = cognito.generate_auth(req_data)
    client = boto3.client('cognito-idp')
    try:
        body = cognito.generate_token(client, auth, req_data)
        return Response(status_code=200, body=body, headers={'Content-Type': 'application/json'})
    except client.exceptions.NotAuthorizedException as e:
        raise BadRequestError(e.response['Error']['Message'])
    except Exception as e:
        raise BadRequestError(e.response['Error']['Message'])


@app.route('/users/signup', methods=['POST'],
           cors=cors_config, content_types=['application/json'])
def signup():
    """
    Sign up to get Cloudalbum service account
    :return:
    """
    req_data = app.current_request.json_body
    dig = cognito.generate_digest(req_data)
    client = boto3.client('cognito-idp')
    try:
        cognito.signup(client, req_data, dig)
        return Response(status_code=201, body={'ok': True},
                        headers={'Content-Type': 'application/json'})
    except client.exceptions.UsernameExistsException as e:
        raise ConflictError(e.response['Error']['Message'])
    except client.exceptions.InvalidParameterException as e:
        raise BadRequestError(e.response['Error']['Message'])
    except client.exceptions.InvalidPasswordException as e:
        raise BadRequestError(e.response['Error']['Message'])
    except ParamValidationError as e:
        raise BadRequestError(e)
    except Exception as e:
        raise ChaliceViewError(e)

@app.route('/users/signout', methods=['POST'], cors=cors_config,
           authorizer=jwt_auth, content_types=['application/json'])
def signout():
    """
    Revoke current access token.
    :return:
    """
    access_token = cognito.get_token(app.current_request)
    client = boto3.client('cognito-idp')
    response = client.global_sign_out(
        AccessToken=access_token
    )
    app.log.debug('Access token expired: {0}'.format(access_token))
    return Response(status_code=200, body={'ok': True},
                    headers={'Content-Type': 'application/json'})

