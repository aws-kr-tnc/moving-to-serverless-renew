import json
import time
import requests
from functools import wraps
from flask import request, jsonify, make_response
from sqlalchemy.orm.exc import NoResultFound
from jose import jwk, jwt
from jose.utils import base64url_decode
from flask import current_app as app

from cloudalbum.solution import solution_get_cognito_user_data

POOL_KEYS = None
blacklist_set = set()

def add_token_to_set(token):
    """
    Adds a new token to the set. It is not revoked when it is added.
    :param identity_claim:
    """
    claims= token_decoder(token)
    jti = claims['jti']
    blacklist_set.add(jti)

def is_blacklisted_token_set(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        if jti in blacklist_set:
            return True
    except NoResultFound:
        return False

def set_cognito_data_global():
    global POOL_KEYS
    POOL_URL = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(app.config['AWS_REGION'],
                                                                                      app.config['COGNITO_POOL_ID'])
    if POOL_KEYS is None:
        aws_data = requests.get(POOL_URL)
        POOL_KEYS = json.loads(aws_data.text)['keys']
        app.logger.debug("COGNITO POOL_KEYS SET DONE!")

def token_decoder(token):
    set_cognito_data_global()

    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']

    result = {}
    for item in POOL_KEYS:
        result[item['kid']] = item

    public_key = jwk.construct(result.get(kid))

    message, encoded_signature = str(token).rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    if not public_key.verify(message.encode("utf8"), decoded_signature):
        app.logger.error('Signature verification failed')
        raise Exception
    app.logger.debug('Signature successfully verified')

    claims = jwt.get_unverified_claims(token)

    if time.time() > claims['exp']:
        app.logger.error('Token is expired')
        raise Exception
    app.logger.debug(claims)
    return claims


def cog_jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return make_response(jsonify({'msg':'no token'}), 400)

        token = request.headers['Authorization']

        try:
            if token_decoder(token.rsplit(' ', 1)[1]) is not None:
                return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return make_response(jsonify({'msg':'invalid token'}), 400)

    return decorated_function

def get_cognito_user(access_token):
    # TODO 8: Implement follwing solution code to get user data from Cognito user pool
    return solution_get_cognito_user_data(access_token)


def get_token_from_header(request):
    return request.headers['Authorization'].rsplit(' ', 1)[1]