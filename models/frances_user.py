from models.pydantic_object_id import PydanticObjectId
from typing import List

class FrancesUserDB:
    id: str
    cbu:str
    balance:int
    name:str
    transfers: List[PydanticObjectId]

    def __init__(self, id:str, name:str, cbu:str,balance:int, transfers:List):
        self.id = id
        self.name = name
        self.cbu = cbu
        self.balance = balance
        self.transfers = transfers

    @classmethod
    def from_json(cls, json:any):
        return cls(
            id = json["_id"],
            name=json["name"],
            cbu=json["cbu"],
            balance=json["balance"],
            transfers=json["transfers"]
        )

class FrancesUserDTO:
    id: str
    cbu:str
    name:str

    def __init__(self, id:str, name:str, cbu:str):
        self.id = id
        self.name = name
        self.cbu = cbu

    @classmethod
    def from_json(cls, json:any):
        return cls(
            id = json["_id"],
            name=json["name"],
            cbu=json["cbu"]
        )
    
    @classmethod
    def from_user(cls, user:FrancesUserDB):
        return cls(
            id = user.id,
            name=user.name,
            cbu=user.cbu
        )