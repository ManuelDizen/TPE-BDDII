import couchdb2
from os import getenv
from dao.frances_user_dao import FrancesUserDao
from dao.frances_transfer_dao import FrancesTransferDao
class CouchAdmin():
    server = any
    user_db = any
    transfer_db = any
    frances_user_dao = FrancesUserDao
    frances_transfer_dao = FrancesTransferDao

    def start_connection(self):
        server = couchdb2.Server(href=getenv("COUCH_URL"), username=getenv("COUCH_USER"), password=getenv("COUCH_PASSWORD"))
        self.server = server
        if server.up() is True:
            print("Server funca")

        db_name = getenv("COUCH_DB_USERS_NAME")
        if db_name in server:
            db = server[db_name]
            print("Base ya existe")
        else:
            db = server.create(db_name)
            print("Creo base")
        
        self.user_db = db

        db_name = getenv("COUCH_DB_TRANSFERS_NAME")
        if db_name in server:
            db = server[db_name]
            print("Base ya existe")
        else:
            db = server.create(db_name)
            print("Creo base")
        
        self.transfer_db = db
        
        with open('config/cbus.txt', 'r') as file:
            cbus = file.read().splitlines()
        cbu_frances = cbus[2]

        self.frances_user_dao = FrancesUserDao(self.user_db, int(cbu_frances))
        self.frances_transfer_dao = FrancesTransferDao(self.transfer_db)

    def close_connection(self):
        self.server.close()

    def get_frances_user_dao(self):
        return self.frances_user_dao
    
    def get_frances_transfer_dao(self):
        return self.frances_transfer_dao