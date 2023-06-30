from pydantic import BaseModel
from fastapi import Request


class GaliciaUserDB(BaseModel):
    cbu:str
    balance:str
    name:str

class GaliciaUserDTO(BaseModel):
    cbu:str
    name:str
    this:str

    @classmethod
    def from_user(cls, user: GaliciaUserDB, request: Request):
        if user is None:
            print("USER ES NONE")
        else:
            print(user.name + " " + user.cbu)

        url = str(request.url_for("get_user_by_cbu", cbu=user.cbu))
        return cls(
            cbu=user.cbu, 
            name=user.name,
            this=url,
        )
