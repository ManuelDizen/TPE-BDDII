from typing import Optional, List

class PixUserDB():
    id: int
    cuit: str
    name: Optional[str]
    mail: Optional[str]
    phone: Optional[str]
    bank_accounts: List[int]

class PixUserDTO():
    cuit:str
    name:Optional[str]
    mail:Optional[str]
    phone:Optional[str]

    def __init__(self, cuit, name, mail=None, phone=None):
        self.cuit = cuit
        self.name = name
        self.mail = mail
        self.phone = phone

    @classmethod
    def create_dto(cls, cuit, name, mail=None, phone=None):
        return cls(
            cuit=cuit,
            name=name,
            mail=mail,
            phone=phone
        )