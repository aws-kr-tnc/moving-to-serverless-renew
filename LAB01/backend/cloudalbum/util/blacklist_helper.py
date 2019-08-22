
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

# from exceptions import TokenNotFound
from cloudalbum.database.models import BlacklistToken
from cloudalbum import db

def add_token_to_database(decoded_token):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """

    jti = decoded_token['jti']

    db_token = BlacklistToken(
        token=jti
    )
    db.session.add(db_token)
    db.session.commit()

def is_blacklisted_token_db(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        is_blacklisted = BlacklistToken.query.filter_by(token=jti).one()
        if is_blacklisted is not None:
            return True
    except NoResultFound:
        return False


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
        if is_blacklisted in blacklist_set:
            return True
    except NoResultFound:
        return False


