from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from models.galicia_user import GaliciaUserDB
from models.pydantic_object_id import PydanticObjectId
# Para CBU, numero de banco: 007. Numero de sucursal: 0001
# "Dicho patrón es 7139713 para el primer bloque, y 3971397139713 para el segundo bloque. "

class GaliciaUserDao:
    galicia_users: Collection
    base_cbu_block: int

    def __init__(self, db: Database, base_cbu_block: int):
        self.galicia_users = db.galicia_users
        self.base_cbu_block = base_cbu_block

    def get_user_by_cbu(self, cbu: str):
        user = self.galicia_users.find_one(
            {"cbu":cbu}
        )
        if user is None:
            return None
        return GaliciaUserDB(**user)
    
    def get_user_by_name(self, name:str):
        user = self.galicia_users.find_one({"name":name})
        if user is None:
            return None
        return GaliciaUserDB(**user)
    
    def get_user_by_cuit(self, cuit:str):
        user = self.galicia_users.find_one({"cuit":cuit})
        if user is None:
            return None
        return GaliciaUserDB(**user)

    def create_user(self, cuit:str, name:str):
        if self.get_user_by_cuit(cuit) is not None:
            return None
        cbu = "00700016" + str(self.base_cbu_block)
        self.base_cbu_block += 1
        try:
            self.galicia_users.insert_one(
                {
                    "cbu":cbu,
                    "cuit":cuit,
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
        self.galicia_users.update_one(
            {"cbu":cbu},
            {"$set":{
                "balance": int(user.balance) - amount
            }}
        )

    def deposit_to_account(self, cbu:str, amount:int):
        print("Entro al get")

        user = self.get_user_by_cbu(cbu)

        print("No es en el get")

        self.galicia_users.update_one(
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
        self.galicia_users.update_one(
            {"cbu":sending_user.cbu},
            {"$push": {"transfers" : transfer_id}},
        )

    def receive_transfer(self, transfer_id:PydanticObjectId, dst_cbu:str,):
        receiving_user = self.get_user_by_cbu(dst_cbu)
        if receiving_user is None:
            return None
        # transfer = self.transfer_dao.create_transfer(src_cbu, dst_cbu, src_bank, "GAL", amount) # Se hardcodea GAL acá porque es el qu emaneja la base de galicia
        if transfer_id is None:
            return None
        self.galicia_users.update_one(
            {"cbu":dst_cbu},
            {"$push":{"transfers":transfer_id},}
        )