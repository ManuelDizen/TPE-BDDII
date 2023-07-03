from typing import Optional, List

class PixUserDB():
    cuit: str
    name: Optional[str]
    mail: Optional[str]
    phone: Optional[str]
    bank_accounts: List[int]