from models.pydantic_object_id import PydanticObjectId
from typing import List

class FrancesUserDB:
    _id: str
    cbu:str
    balance:int
    name:str
    transfers: List[PydanticObjectId]

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