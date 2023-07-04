import couchdb2
from couchdb2 import Database
from os import getenv
import requests
import json
from models.frances_user import FrancesUserDTO
# Codigo de banco 017

class FrancesUserDao:

    db: Database
    base_cbu_block:int

    def __init__(self, db:Database, base_cbu_block:int):
        #self.db = db[getenv("COUCH_DB_USERS_NAME")]
        self.db = db
        self.base_cbu_block = base_cbu_block

    def create_user(self, name:str):
        cbu = "01700016" + str(self.base_cbu_block)
        self.base_cbu_block += 1
        user = {"cbu":cbu, "name":name, "balance":0, "transfers":[]}
        self.db.put(user)
        return 
    
    def get_user_by_cbu(self, cbu:str):
        query = {
            'selector': {
                "cbu": cbu
            },
            'limit': 1
        }
        response = requests.post(
            'http://admin:tpebdd2@localhost:5984/frances_users/_find', json=query
        ) #TODO: Method that creates this url based on env variables

        json_response = json.loads(response.text)
        print(json_response)
        #TODO: Devolver un tipo UserDB

        return FrancesUserDTO.from_json(json_response["docs"][0])
    
    def extract_from_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        if "cbu" not in user["docs"][0]:
            return 404
        print(user["docs"][0])
        current_balance = user["docs"][0]["balance"]

        if current_balance < amount:
            return 400 #Not enough funds
        
        new_balance = current_balance - amount
        body = {
            "name":user["docs"][0]["name"],
            "cbu":user["docs"][0]["cbu"],
            "balance":new_balance, 
            "_rev":user["docs"][0]["_rev"]
            }
        print(body)
        url = 'http://admin:tpebdd2@localhost:5984/frances_users/{}'.format(
            user["docs"][0]["_id"]
        )
        response = requests.put(url, json.dumps(body))
        json_response = json.loads(response.text)
        if "error" in json_response:
            return -1
        
        return 0
        
    def deposit_to_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        if "cbu" not in user["docs"][0]:
            return 404
        current_balance = user["docs"][0]["balance"]
        new_balance = current_balance + amount
        body = {
            "name":user["docs"][0]["name"],
            "cbu":user["docs"][0]["cbu"],
            "balance":new_balance, 
            "_rev":user["docs"][0]["_rev"]
            }
        print(body)
        url = 'http://admin:tpebdd2@localhost:5984/frances_users/{}'.format(
            user["docs"][0]["_id"]
        )
        response = requests.put(url, json.dumps(body))
        json_response = json.loads(response.text)
        if "error" in json_response:
            return -1
        return 0

    def get_base_cbu(self):
        return self.base_cbu_block