from pydantic import Field
from fastapi import Request
from typing import Optional
from models.pydantic_object_id import PydanticObjectId

class FTransferDB:
    id: str
    src_cbu: str
    src_bank: Optional[str]
    dst_cbu: str
    dst_bank: Optional[str]
    amount: int
    #TODO: Acá le podría poner algún enum para tener "estado de transferencia",
    # cosa que si hay algún problema en al realización de la misma,
    # quede flaggeada en la cuenta como "no completada"

class FTransferDTO:
    id: str
    src_cbu: str
    src_bank: Optional[str]
    dst_cbu: str
    dst_bank: Optional[str]
    amount: int

    def __init__(self, id:str, src_cbu:str, src_bank: str, dst_cbu:str, dst_bank:str, amount:int):
        self.id=id
        self.amount=amount
        self.src_bank = src_bank
        self.src_cbu=src_cbu
        self.dst_bank=dst_bank
        self.dst_cbu=dst_cbu

    @classmethod
    def from_transfer(cls, id:str, src_cbu:str, src_bank: str, dst_cbu:str, dst_bank:str, amount:int):
        return cls(
            id=id,
            amount=amount,
            src_bank = src_bank,
            src_cbu=src_cbu,
            dst_bank=dst_bank,
            dst_cbu=dst_cbu
        )