from models.pydantic_object_id import PydanticObjectId
from typing import List

class FrancesUserDB:
    id: str
    cbu:str
    balance:int
    cuit:str
    name:str
    transfers: List[PydanticObjectId]
    rev :str

    def __init__(self, id:str, cuit: str, name:str, cbu:str, balance:int, transfers:List, rev:str):
        self.id = id
        self.cuit = cuit
        self.name = name
        self.cbu = cbu
        self.balance = balance
        self.transfers = transfers
        self.rev = rev

    @classmethod
    def from_json(cls, json:any):
        return cls(
            id = json["_id"],
            name=json["name"],
            cuit=json["cuit"],
            cbu=json["cbu"],
            balance=json["balance"],
            transfers=json["transfers"],
            rev=json["_rev"]
        )

class FrancesUserDTO:
    id: str
    cbu:str
    cuit:str
    name:str

    def __init__(self, id:str, cuit: str, name:str, cbu:str):
        self.id = id
        self.name = name
        self.cuit = cuit
        self.cbu = cbu

    @classmethod
    def from_json(cls, json:any):
        return cls(
            id = json["_id"],
            cuit=json["cuit"],
            name=json["name"],
            cbu=json["cbu"]
        )
    
    @classmethod
    def from_user(cls, user:FrancesUserDB):
        return cls(
            id = user.id,
            cuit=user.cuit,
            name=user.name,
            cbu=user.cbu
        )