"""
    cloudalbum/database/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Functions for DB table handling

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""

from cloudalbum.database.model_ddb import User, Photo
from flask import current_app as app


def create_table():
    if not User.exists():
        app.logger.debug('Creating DynamoDB User table..')
        User.create_table(read_capacity_units=app.config['DDB_RCU'],
                          write_capacity_units=app.config['DDB_WCU'],
                          wait=True)
    if not Photo.exists():
        app.logger.debug('Creating DynamoDB Photo table..')
        Photo.create_table(read_capacity_units=app.config['DDB_RCU'],
                           write_capacity_units=app.config['DDB_WCU'],
                           wait=True)


def delete_table():
    if User.exists():
        User.delete_table()
    if Photo.exists():
        Photo.delete_table()
