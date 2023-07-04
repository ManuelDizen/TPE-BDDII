from couchdb2 import Database
import requests
import json
from models.transfer_2 import FTransferDB, FTransferDTO
class FrancesTransferDao:
    db: Database
    base_transfer_block: int

    def __init__(self, db:Database, base_transfer_block:int):
        self.db = db
        self.base_transfer_block = base_transfer_block

    def get_base_transfer(self):
        return self.base_transfer_block

    def create_transfer(self, src_cbu:str, dst_cbu:str, src_bank:str, dst_bank:str, amount:int):
        new_transfer = {
            "_id":str(self.base_transfer_block),
            "src_cbu":src_cbu, 
            "dst_cbu":dst_cbu, 
            "src_bank":src_bank, 
            "dst_bank":dst_bank, 
            "amount":amount
            }
        url = 'http://admin:tpebdd2@localhost:5984/frances_transfers/{}'.format(self.base_transfer_block)
        response = requests.put(url, json.dumps(new_transfer))
        json_response = json.loads(response.text)
        if "error" in json_response:
            print(json_response)
            return -1
        print(json_response)
        self.base_transfer_block += 1
        return self.get_transfer_by_id(self.base_transfer_block - 1)
    
    def get_transfer_by_id(self, id: str):
        query = {
            'selector': {
                "_id": str(id)
            },
            'limit': 1
        }   
        print(query)
        response = requests.post(
            'http://admin:tpebdd2@localhost:5984/frances_transfers/_find', json=query
        ) #TODO: Method that creates this url based on env variables

        json_response = json.loads(response.text)
        print(json_response)
        #TODO: Cambiar para traer un tipo TransferDB
        json_obj = json_response["docs"][0]
        transfer = FTransferDTO.from_transfer(json_obj["_id"], json_obj["src_cbu"], json_obj["src_bank"],
                                              json_obj["dst_cbu"], json_obj["dst_bank"], json_obj["amount"])
        return transfer