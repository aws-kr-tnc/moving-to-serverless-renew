import json
import time
import requests
from functools import wraps
from flask import request, jsonify, make_response
from sqlalchemy.orm.exc import NoResultFound
from jose import jwk, jwt
from jose.utils import base64url_decode
from flask import current_app as app

from project.util.config import conf

POOL_KEYS = None
blacklist_set = set()
def add_token_to_set(decoded_token):
    """
    Adds a new token to the set. It is not revoked when it is added.
    :param identity_claim:
    """

    jti = decoded_token['jti']
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
    if POOL_KEYS is None:
        aws_data = requests.get('https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(conf['AWS_REGION'],
                                                                                      conf['COGNITO_POOL_ID']))
        POOL_KEYS = json.loads(aws_data.text)['keys']
        print("POOL_KEYS SET ")

def token_decoder(token, audience=None):
    set_cognito_data_global()

    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']

    result = {}
    for item in POOL_KEYS:
        result[item['kid']] = item

    public_key = jwk.construct(result.get(kid))

    kargs = {"issuer": ""}
    if audience is not None:
        kargs["audience"] = audience

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


def pyjwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return make_response(jsonify({'msg':'no token'}), 400)

        token = request.headers['Authorization']

        try:
            if token_decoder(token.rsplit(' ', 1)[1], None) is not None:
                return f(*args, **kwargs)
            else:
                return make_response(jsonify({'msg': 'invalid token'}), 400)
        except:
            return make_response(jsonify({'msg':'invalid token'}), 400)

    return decorated_function

