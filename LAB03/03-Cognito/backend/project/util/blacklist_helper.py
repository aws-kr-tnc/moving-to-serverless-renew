import base64
import hashlib
import hmac
import json
import time
import urllib
from functools import wraps

from flask import request, jsonify, make_response
from sqlalchemy.orm.exc import NoResultFound
# import jwt
from jose import jwk, jwt
from jose.utils import base64url_decode
from flask import current_app as app

from project.util.config import conf

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



def token_decoder(token):


    keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(conf['AWS_REGION'], conf['COGNITO_POOL_ID'])
    # instead of re-downloading the public keys every time
    # we download them only on cold start
    # https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
    response = urllib.request.urlopen(keys_url)
    keys = json.loads(response.read())['keys']
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1

    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        app.logger.error('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        app.logger.error('Signature verification failed')
        return False
    app.logger.debug('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        app.logger.error('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    #
    # if claims['aud'] != conf['COGNITO_CLIENT_ID']:
    #     app.logger.error('Token was not issued for this audience')
    #     return False
    # now we can use the claims
    app.logger.debug(claims)
    return True


def jwt_test(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return make_response(jsonify({'msg':'no token'}), 400)

        token = request.headers['Authorization']
        result_token= None
        try:
            if token_decoder(token.rsplit(' ', 1)[1]):
                return f(*args, **kwargs)
            else:
                return make_response(jsonify({'msg': 'invalid token'}), 400)
        except:
            return make_response(jsonify({'msg':'invalid token'}), 400)

    return decorated_function

