from pydantic import BaseModel
from fastapi import Request
from models.pydantic_object_id import PydanticObjectId
from typing import List

class SantanderUserDB(BaseModel):
    cbu:str
    balance:int
    name:str
    transfers: List[PydanticObjectId]

class SantanderUserDTO(BaseModel):
    cbu:str
    name:str
    this:str

    @classmethod
    def from_user(cls, user: SantanderUserDB, request: Request):
        url = str(request.url_for("get_user_by_cbu", cbu=user.cbu))
        return cls(
            cbu=user.cbu, 
            name=user.name,
            this=url,
        )
