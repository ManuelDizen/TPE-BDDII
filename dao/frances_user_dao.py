import couchdb2
from couchdb2 import Database
from os import getenv
import requests
import json
from models.frances_user import FrancesUserDTO, FrancesUserDB
from models.pydantic_object_id import PydanticObjectId

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
        # user = {"cbu":cbu, "name":name, "balance":0, "transfers":[]}
        # self.db.put(user)
        body = {
            "name":name,
            "cbu":str(cbu),
            "balance":0, 
            "transfers":[],
            }
        url = 'http://admin:tpebdd2@localhost:5984/frances_users/{}'.format(cbu)
        response = requests.put(url, json.dumps(body))
        json_response = json.loads(response.text)
        if "error" in json_response:
            print(json_response)
            return -1
        print(json_response)
        return self.get_user_by_cbu(str(cbu))
        # TODO: Cachear posible error (aunque no veo porque debería ocurrir)
    
    def get_user_by_cbu(self, cbu:str):
        print(cbu)
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
        #TODO: Cachear un error y devolver None
        return FrancesUserDB.from_json(json_response["docs"][0])

    def get_user_by_name(self, name:str):
        query = {
            'selector': {
                "name": name
            },
            'limit': 1
        }
        response = requests.post(
            'http://admin:tpebdd2@localhost:5984/frances_users/_find', json=query
        ) #TODO: Method that creates this url based on env variables

        json_response = json.loads(response.text)
        #TODO: Cachear un error y devolver None

        print(json_response)

        return FrancesUserDB.from_json(json_response["docs"][0])
    
    def extract_from_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        if user is None:
            return 404
        current_balance = user.balance

        if current_balance < amount:
            return 400 #Not enough funds
        
        new_balance = current_balance - amount
        body = {
            "name":user.name,
            "cbu":user.cbu,
            "balance":new_balance, 
            "transfers":user.transfers,
            "_rev":user.rev
            }
        print(body)
        url = 'http://admin:tpebdd2@localhost:5984/frances_users/{}'.format(
            user.id
        )
        response = requests.put(url, json.dumps(body))
        json_response = json.loads(response.text)
        if "error" in json_response:
            return -1
        
        return 0
        
    def deposit_to_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        if user is None:
            return 404
        current_balance = user.balance
        new_balance = current_balance + amount
        body = {
            "name":user.name,
            "cbu":user.cbu,
            "balance":new_balance, 
            "transfers":user.transfers,
            "_rev":user.rev
            }
        print(body)
        url = 'http://admin:tpebdd2@localhost:5984/frances_users/{}'.format(
            user.id
        )
        response = requests.put(url, json.dumps(body))
        json_response = json.loads(response.text)
        if "error" in json_response:
            return -1
        return 0
    
    def transfer_to_account(self, transfer_id:PydanticObjectId, src_cbu:str):
        user = self.get_user_by_cbu(src_cbu)
        if user is None or transfer_id is None:
            return None
        user.transfers.append(transfer_id)
        body = {
            "name":user.name,
            "cbu":user.cbu,
            "balance":user.balance, 
            "transfers":user.transfers,
            "_rev":user.rev
            }
        print(body)
        url = 'http://admin:tpebdd2@localhost:5984/frances_users/{}'.format(
            user.id
        )
        response = requests.put(url, json.dumps(body))
        json_response = json.loads(response.text)
        if "error" in json_response:
            return -1
        return 0

    def receive_transfer(self, transfer_id:PydanticObjectId, dst_cbu:str,):
        user = self.get_user_by_cbu(dst_cbu)
        if user is None or transfer_id is None:
            return None
        user.transfers.append(transfer_id)
        body = {
            "name":user.name,
            "cbu":user.cbu,
            "balance":user.balance, 
            "transfers":user.transfers,
            "_rev":user.rev
            }
        print(body)
        url = 'http://admin:tpebdd2@localhost:5984/frances_users/{}'.format(
            user.id
        )
        response = requests.put(url, json.dumps(body))
        json_response = json.loads(response.text)
        if "error" in json_response:
            return -1
        return 0

    def get_balance_by_cbu(self, cbu:str):
        user = self.get_user_by_cbu(cbu)
        if user is None:
            return -1
        return user.balance

    def get_base_cbu(self):
        return self.base_cbu_block