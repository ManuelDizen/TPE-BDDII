from pymongo.database import Database
from pymongo.collection import Collection
from models.santander_user import SantanderUserDB
from models.transfer import TransferDB
from dao.santander_user_dao import SantanderUserDao

class SantanderTransferDao:
    santander_transfers: Collection

    def __init__(self, db: Database):
        self.santander_transfers = db.santander_transfers

    def create_transfer(self, src_cbu:str, dst_cbu:str, src_bank:str, dst_bank:str, amount:int):
        try:
            new_transfer = self.santander_transfers.insert_one(
                {
                    "src_cbu":src_cbu,
                    "dst_cbu":dst_cbu,
                    "src_bank":src_bank,
                    "dst_bank":dst_bank,
                    "amount":amount
                }
            )
        except Exception:
            raise Exception("Error creating transfer")
        return self.get_transfer_by_id(new_transfer.inserted_id)
    
    def get_transfer_by_id(self, id: str):
        transfer = self.santander_transfers.find_one({"_id":id})
        return TransferDB(**transfer) if transfer is not None else None