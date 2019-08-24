from cloudalbum.util.config import conf
from cloudalbum.database.model_ddb import Photo
from flask import current_app as app

if not Photo.exists():
    Photo.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    app.logger.debug('DynamoDB Photo table created!')

def create_table():
    Photo.create_table()
    app.logger.debug("Dynamodb Photos table created")

def delete_table():
    Photo.delete_table()
    app.logger.debug("Dynamodb Users table deleted")
