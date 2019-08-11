
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

# from exceptions import TokenNotFound
from project.api.models import BlacklistToken
from project import db

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

def is_blacklisted_token(decoded_token):
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


