from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from models.galicia_user import GaliciaUserDB
from models.transfer import TransferDB
from dao.galicia_user_dao import GaliciaUserDao

class GaliciaTransferDao:
    transfers: Collection

    def __init__(self, db: Database):
        self.transfers = db.transfers

    def create_transfer(self, src_cbu:str, dst_cbu:str, src_bank:str, dst_bank:str, amount:int):
        try:
            new_transfer = self.transfers.insert_one(
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
        transfer = self.transfers.find_one({"_id":id})
        return TransferDB(**transfer) if transfer is not None else None