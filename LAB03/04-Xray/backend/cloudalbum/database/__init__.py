from cloudalbum.util.config import conf
from cloudalbum.database.model_ddb import Photo

if not Photo.exists():
    Photo.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    print('DynamoDB Photo table created!')

def create_table():
    Photo.create_table()
    print("Dynamodb Photos table created")
    pass

def delete_table():
    Photo.delete_table()
    print("Dynamodb Users table deleted")
