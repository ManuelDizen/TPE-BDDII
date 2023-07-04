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

def get_frances_user_dao():
    return couch.get_frances_user_dao()

def save_updated_cbus():
    with open('config/cbus.txt', 'w') as file:
        file.write(str(get_galicia_user_dao().get_base_cbu()) + '\n')
        file.write(str(get_santander_user_dao().get_base_cbu()) + '\n')
        file.write(str(get_frances_user_dao().get_base_cbu()) + '\n')