import couchdb2
from os import getenv
class CouchAdmin():
    server = any
    db = any

    def start_connection(self):
        server = couchdb2.Server(href=getenv("COUCH_URL"), username=getenv("COUCH_USER"), password=getenv("COUCH_PASSWORD"))
        self.server = server
        if server.up() is True:
            print("Server funca")

        db_name = getenv("COUCH_DB_NAME")
        if db_name in server:
            db = server[db_name]
            print("Base ya existe")
        else:
            db = server.create(db_name)
            print("Creo base")
        self.db = db
        
        users_collection_name = getenv("COUCH_DB_USERS_NAME")

        if users_collection_name not in db:
            users_collection_doc = {'_id':'frances_users'}
            db.put(users_collection_doc)  
            print("GUARDIAN PRINT: SI SALE ALERTARSE")

        transfers_collection_name = getenv("COUCH_DB_TRANSFERS_NAME")
        if transfers_collection_name not in db:
            users_collection_doc = {'_id':'frances_transfers'}
            db.put(transfers_collection_name) 
            print("GUARDIAN PRINT: SI SALE ALERTARSE")


    def close_connection(self):
        self.server.close()
