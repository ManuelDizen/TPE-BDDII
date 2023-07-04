from config.mongo_admin import MongoAdmin
from config.postgres_admin import PostgresAdmin
from config.couch_admin import CouchAdmin

mongo = MongoAdmin()
postgres = PostgresAdmin()
couch = CouchAdmin()

def get_galicia_user_dao():
    return mongo.get_galicia_user_dao()

def get_galicia_transfer_dao():
    return mongo.get_galicia_transfer_dao()

def get_santander_user_dao():
    return mongo.get_santander_user_dao()

def get_santander_transfer_dao():
    return mongo.get_santander_transfer_dao()

def get_pix_user_dao():
    return postgres.get_pix_user_dao()