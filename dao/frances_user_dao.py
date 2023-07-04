import couchdb2
from couchdb2 import Database
from os import getenv

# Codigo de banco 017

class FrancesUserDao:

    db: Database
    base_cbu_block:int

    def __init__(self, db:Database, base_cbu_block:int):
        #self.db = db[getenv("COUCH_DB_USERS_NAME")]
        self.db = db
        print(self.db)
        self.base_cbu_block = base_cbu_block

    def create_user(self, name:str):
        cbu = "01700016" + str(self.base_cbu_block)
        self.base_cbu_block += 1
        user = {"cbu":cbu, "name":name, "balance":0, "transfers":[]}
        self.db.put(user)
        return 
    
    def find_user_by_cbu(self, cbu:str):
        return

    def get_base_cbu(self):
        return self.base_cbu_block