from couchdb2 import Database
import requests
import json

class FrancesTransferDao:
    db: Database

    def __init__(self, db:Database):
        self.db = db

    def create_transfer(self, src_cbu:str, dst_cbu:str, src_bank:str, dst_bank:str, amount:int):
        new_transfer = {"src_cbu":src_cbu, "dst_cbu":dst_cbu, "src_bank":src_bank, "dst_bank":dst_bank, "amount":amount}
        self.db.put(new_transfer)

        #TODO: Cambiar para que devuela un tipo "TransferDB"

        return 0
    
    def get_transfer_by_id(self, id: str):
        query = {
            'selector': {
                "_id": id
            },
            'limit': 1
        }   
        response = requests.post(
            'http://admin:tpebdd2@localhost:5984/frances_transfers/_find', json=query
        ) #TODO: Method that creates this url based on env variables

        json_response = json.loads(response.text)
        #print(json_response)
        #TODO: Cambiar para traer un tipo TransferDB
        return json_response