import couchdb2

class CouchAdmin():
    server = any
    db = any

    def start_connection(self):
        server = couchdb2.Server(href='http://localhost:5984', username='admin', password='tpebdd2')
        self.server = server
        if server.up() is True:
            print("Server funca")

        db_name = 'frances'
        if db_name in server:
            db = server[db_name]
            print("Base ya existe")
        else:
            db = server.create(db_name)
            print("Creo base")
        self.db = db
        
        users_collection_name = 'frances_users'

        test = db.get('frances_users')
        print(test)
        test = db.get('frances_transfers')
        print(test)

        if users_collection_name not in db:
            users_collection_doc = {'_id':'frances_users'}
            db.put(users_collection_doc)  
            print("entre a putear igual!")

        transfers_collection_name = 'frances_transfers'
        if transfers_collection_name not in db:
            users_collection_doc = {'_id':'frances_transfers'}
            db.put(transfers_collection_name) 
            print("entre a putear igual en transfers!Eii32i1!")


    def close_connection(self):
        self.server.close()
