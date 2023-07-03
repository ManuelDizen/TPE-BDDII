class PixBankAccount:
    id: int
    bank_id: int
    cbu: str 

    def __init__(self, id: int, bank_id: int, cbu: str):
        self.id = id
        self.bank_id = bank_id
        self.cbu = cbu