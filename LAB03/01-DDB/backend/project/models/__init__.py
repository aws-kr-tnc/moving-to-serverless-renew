from flask import app
from project.util.config import conf
from project.models.ddb import User


if not User.exists():

    User.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    print('DynamoDB User table created!')

def create_table():
    User.create_table()
    print("Dynamodb Users table created")
    pass

def delete_table():
    User.delete_table()
    print("Dynamodb Users table deleted")
