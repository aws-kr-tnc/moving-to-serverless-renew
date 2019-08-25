"""
    cloudalbum/chalicelib/cognito.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Functions for AWS Cognito access.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import base64
import hashlib
import hmac
import json
import time
import boto3
import requests
from jose import jwk, jwt
from chalicelib.config import conf
from chalice import UnauthorizedError
from jose.utils import base64url_decode

POOL_KEYS = None
POOL_URL = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.\
    format(conf['AWS_REGION'], conf['COGNITO_POOL_ID'])


def remove_barer(token):
    return token.replace('Bearer ', '')


def generate_digest(req_data):
    """
    Generate HMAC digest code.
    :param req_data:
    :return:
    """
    msg = '{0}{1}'.format(req_data['email'], conf['COGNITO_CLIENT_ID'])
    dig = hmac.new(conf['COGNITO_CLIENT_SECRET'].encode('utf-8'),
                   msg=msg.encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    return dig


def signup(client, user, dig):
    """
    Register a user to Cognito User Pool
    :param client:
    :param user:
    :param dig:
    :return:
    """
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
    client.admin_confirm_sign_up(
        UserPoolId=conf['COGNITO_POOL_ID'],
        Username=id
    )
    return {'email': email, 'id': id}


def generate_token(client, auth, req_data):
    """
    Retrieve JWT tokens for authentication.
    :param client:
    :param auth:
    :param req_data:
    :return:
    """
    resp = client.admin_initiate_auth(
        UserPoolId=conf['COGNITO_POOL_ID'],
        ClientId=conf['COGNITO_CLIENT_ID'],
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={'SECRET_HASH': auth,
                        'USERNAME': req_data['email'],
                        'PASSWORD': req_data['password']})
    access_token = resp['AuthenticationResult']['AccessToken']
    refresh_token = resp['AuthenticationResult']['RefreshToken']
    res_body = {"accessToken": access_token, "refreshToken": refresh_token}
    return res_body


def set_cognito_data_global():
    global POOL_KEYS
    if POOL_KEYS is None:
        aws_data = requests.get(POOL_URL)
        POOL_KEYS = json.loads(aws_data.text)['keys']


def token_decoder(token):
    """
    The ID token expires one hour after the user authenticates.
    You should not process the ID token in your client or web API after it has expired.
    https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html
    :param token:
    :return:
    """
    set_cognito_data_global()
    token = remove_barer(token)

    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']

    result = {}
    for item in POOL_KEYS:
        result[item['kid']] = item

    public_key = jwk.construct(result.get(kid))

    message, encoded_signature = str(token).rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    if not public_key.verify(message.encode("utf8"), decoded_signature):
        raise UnauthorizedError('Invalid Token')

    claims = jwt.get_unverified_claims(token)

    if time.time() > claims['exp']:
        raise UnauthorizedError('Token in expired!')
    return claims


def generate_auth(req_data):
    """
    Generate HMAC authentication code.
    :param req_data:
    :return:
    """
    msg = '{0}{1}'.format(req_data['email'], conf['COGNITO_CLIENT_ID'])
    dig = hmac.new(conf['COGNITO_CLIENT_SECRET'].encode('utf-8'),
                   msg=msg.encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    auth = base64.b64encode(dig).decode()
    return auth


def get_token(request):
    """
    Retrieve 'Authorization' header value.
    :param request:
    :return:
    """
    token = request.headers['authorization']
    token = remove_barer(token)
    return token


def user_info(access_token):
    """
    Retrieve user information in the Cognito user pool.
    :param access_token:
    :return:
    """
    client = boto3.client('cognito-idp')
    try:
        cognito_user = client.get_user(AccessToken=access_token)
        user_info = {}
        for attr in cognito_user['UserAttributes']:
            key = attr['Name']
            if key == 'sub':
                key = 'user_id'
            val = attr['Value']
            user_info[key] = val
        return user_info
    except Exception as e:
        raise UnauthorizedError('Token is invalid!')

