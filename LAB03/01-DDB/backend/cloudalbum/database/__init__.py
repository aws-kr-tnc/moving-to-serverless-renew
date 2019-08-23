from cloudalbum.util.config import conf
from cloudalbum.database.model_ddb import User, Photo

if not User.exists():
    User.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    print('DynamoDB User table created!')

if not Photo.exists():
    User.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    print('DynamoDB User table created!')

def create_table():
    User.create_table()
    Photo.create_table()
    print("Dynamodb Users & Photos table created")
    pass

def delete_table():
    User.delete_table()
    Photo.delete_table()
    print("Dynamodb Users & Photos table deleted")
