from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from models.santander_user import SantanderUserDB
from models.pydantic_object_id import PydanticObjectId

# Para CBU, numero de banco: 072. Numero de sucursal: 0001

class SantanderUserDao:
    santander_users: Collection
    base_cbu_block: int

    def __init__(self, db: Database, base_cbu_block: int):
        self.santander_users = db.santander_users
        self.base_cbu_block = base_cbu_block

    def get_user_by_cbu(self, cbu: str):
        user = self.santander_users.find_one(
            {"cbu":cbu}
        )
        if user is None:
            return None
        return SantanderUserDB(**user)
    
    def get_user_by_name(self, name:str):
        user = self.santander_users.find_one({"name":name})
        if user is None:
            return None
        return SantanderUserDB(**user)

    def create_user(self, name:str):
        if self.get_user_by_name(name) is not None:
            return None
        cbu = "07200016" + str(self.base_cbu_block)
        self.base_cbu_block += 1
        try:
            self.santander_users.insert_one(
                {
                    "cbu":cbu,
                    "name":name,
                    "balance":0,
                    "transfers": [],
                }
            )
        except DuplicateKeyError:
            return None
        return self.get_user_by_cbu(cbu)

    def extract_from_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        self.santander_users.update_one(
            {"cbu":cbu},
            {"$set":{
                "balance": int(user.balance) - amount
            }}
        )

    def deposit_to_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        self.santander_users.update_one(
            {"cbu":cbu},
            {"$set":{
                "balance": int(user.balance) + amount
            }}
        )

    def get_base_cbu(self):
        return self.base_cbu_block
    
    # Este endpoint unicamente almacena la transferencia. NO deduce dinero de la cuenta, ni tampoco acredita en la otra
    # SOlo anota en la cuenta de la que se transfiere el registro
    def transfer_to_account(self, transfer_id:PydanticObjectId, src_cbu:str):
        sending_user = self.get_user_by_cbu(src_cbu)
        if sending_user is None:
            return None
        if transfer_id is None:
            return None
        self.santander_users.update_one(
            {"cbu":sending_user.cbu},
            {"$push": {"transfers" : transfer_id}},
        )

    def receive_transfer(self, transfer_id:PydanticObjectId, dst_cbu:str,):
        receiving_user = self.get_user_by_cbu(dst_cbu)
        if receiving_user is None:
            return None
        if transfer_id is None:
            return None
        self.santander_users.update_one(
            {"cbu":dst_cbu},
            {"$push":{"transfers":transfer_id},}
        )