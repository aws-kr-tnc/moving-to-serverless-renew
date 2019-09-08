"""
    cloudalbum/util/blacklist_helper.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Handling JWT token for signed out user.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""


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

    if jti in blacklist_set:
        return True



