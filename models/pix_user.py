from typing import Optional, List

class PixUserDB():
    id: int
    cuit: str
    name: Optional[str]
    mail: Optional[str]
    phone: Optional[str]
    bank_accounts: List[int]