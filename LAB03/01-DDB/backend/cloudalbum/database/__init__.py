from cloudalbum.database.model_ddb import User, Photo
from flask import current_app as app

if not User.exists():
    User.create_table(read_capacity_units=app.config['DDB_RCU'], write_capacity_units=app.config['DDB_WCU'], wait=True)
    app.logger.debug('DynamoDB User table created!')

if not Photo.exists():
    User.create_table(read_capacity_units=app.config['DDB_RCU'], write_capacity_units=app.config['DDB_WCU'], wait=True)
    app.logger.debug('DynamoDB User table created!')


def create_table():
    User.create_table()
    Photo.create_table()
    app.logger.debug("Dynamodb Users & Photos table created")


def delete_table():
    User.delete_table()
    Photo.delete_table()
    app.logger.debug("Dynamodb Users & Photos table deleted")
