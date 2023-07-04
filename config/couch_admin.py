import couchdb2
from os import getenv
from dao.frances_user_dao import FrancesUserDao
class CouchAdmin():
    server = any
    user_db = any
    transfer_db = any
    frances_user_dao = FrancesUserDao

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
        
        """ users_collection_name = getenv("COUCH_DB_USERS_NAME")

        if users_collection_name not in self.user_db:
            users_collection_doc = {'_id':'frances_users'}
            self.user_db.put(users_collection_doc)  
            print("GUARDIAN PRINT: SI SALE ALERTARSE") """

        """ transfers_collection_name = getenv("COUCH_DB_TRANSFERS_NAME")
        if transfers_collection_name not in db:
            users_collection_doc = {'_id':'frances_transfers'}
            db.put(transfers_collection_name) 
            print("GUARDIAN PRINT: SI SALE ALERTARSE") """
        
        with open('config/cbus.txt', 'r') as file:
            cbus = file.read().splitlines()
        cbu_frances = cbus[2]

        self.frances_user_dao = FrancesUserDao(self.user_db, int(cbu_frances))


    def close_connection(self):
        self.server.close()

    def get_frances_user_dao(self):
        return self.frances_user_dao