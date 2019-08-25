import boto3
import logging
from chalice import Chalice, Response, BadRequestError, AuthResponse, ChaliceViewError
from chalicelib import cognito
from chalicelib.model_ddb import Photo, create_photo_info, ModelEncoder
from chalicelib.config import conf, cors_config
from chalicelib.util import pp, save_s3_chalice, get_parts, presigned_url
import uuid
import json
import datetime

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
    try:
        current_user = cognito.user_info(cognito.get_token(app.current_request))
        filename = "{0}.{1}".format(uuid.uuid4(), extension)
        filesize = save_s3_chalice(form['file'][0], filename, current_user['email'], app.log)

        pp.pprint(current_user)
        new_photo = create_photo_info(current_user['user_id'], filename, filesize, form)
        new_photo.save()
        return Response(status_code=200, body={'ok': 'true'},
                        headers={'Content-Type': 'application/json'})
    except Exception as e:
        raise ChaliceViewError(e)


@app.route('/photos', methods=['GET'], cors=cors_config,
           authorizer=jwt_auth, content_types=['application/json'])
def photos():
    current_user = cognito.user_info(cognito.get_token(app.current_request))
    photos = Photo.query(current_user['user_id'])
    data = {'photos': list(photos)}
    body=json.dumps(data, cls=ModelEncoder)

    return Response(status_code=200, body=body,
                    headers={'Content-Type': 'application/json'})


@app.route('/users/signin', methods=['POST'],
           cors=cors_config, content_types=['application/json'])
def signin():
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
    req_data = app.current_request.json_body
    dig = cognito.generate_digest(req_data)
    client = boto3.client('cognito-idp')
    try:
        cognito.signup(client, req_data, dig)
        return Response(status_code=200, body={'ok': 'true'},
                        headers={'Content-Type': 'application/json'})
    except client.exceptions.ParamValidationError as e:
        raise BadRequestError(e.response['Error']['Message'])
    except Exception as e:
        raise BadRequestError(e.response['Error']['Message'])


@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()
