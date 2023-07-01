from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from models.galicia_user import GaliciaUserDB

# Para CBU, numero de banco: 007. Numero de sucursal: 0001
# "Dicho patrón es 7139713 para el primer bloque, y 3971397139713 para el segundo bloque. "

class GaliciaUserDao:
    users: Collection
    base_cbu_block: int

    def __init__(self, db: Database, base_cbu_block: int):
        self.users = db.users
        self.base_cbu_block = base_cbu_block

    def get_user_by_cbu(self, cbu: str):
        user = self.users.find_one(
            {"cbu":cbu}
        )
        if user is None:
            return None
        return GaliciaUserDB(**user)
    
    def get_user_by_name(self, name:str):
        user = self.users.find_one({"name":name})
        if user is None:
            return None
        return GaliciaUserDB(**user)

    def create_galicia_user(self, name:str):
        if self.get_user_by_name(name) is not None:
            return None
        cbu = "00700016" + str(self.base_cbu_block)
        self.base_cbu_block += 1
        try:
            self.users.insert_one(
                {
                    "cbu":cbu,
                    "name":name,
                    "balance":0
                }
            )
        except DuplicateKeyError:
            return None
        return self.get_user_by_cbu(cbu)

    def extract_from_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        self.users.update_one({
            {"_id":user.id}    ,
            {"cbu":cbu},
            {"$set":{
                "amount": user.amount - amount
            }}
        })

    def deposit_to_account(self, cbu:str, amount:int):
        user = self.get_user_by_cbu(cbu)
        self.users.update_one({
            {"cbu":cbu},
            {"$set":{
                "amount": user.amount + amount
            }}
        })

    def get_base_cbu(self):
        return self.base_cbu_block