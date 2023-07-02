from pydantic import BaseModel, Field
from fastapi import Request
from typing import Optional
from models.pydantic_object_id import PydanticObjectId

class TransferDB(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    src_cbu: str
    src_bank: Optional[str]
    dst_cbu: str
    dst_bank: Optional[str]
    amount: int
    #TODO: Acá le podría poner algún enum para tener "estado de transferencia",
    # cosa que si hay algún problema en al realización de la misma,
    # quede flaggeada en la cuenta como "no completada"

class TransferDTO(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    src_cbu: str
    src_bank: Optional[str]
    dst_cbu: str
    dst_bank: Optional[str]
    amount: int

    @classmethod
    def from_transfer(cls, src_cbu:str, src_bank: str, dst_cbu:str, dst_bank:str, amount:int):
        return cls(
            amount=amount,
            src_bank = src_bank,
            src_cbu=src_cbu,
            dst_bank=dst_bank,
            dst_cbu=dst_cbu
        )