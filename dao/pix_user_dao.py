from config.postgres_admin import PostgresAdmin
from config import get_galicia_user_dao, get_galicia_transfer_dao
from models.pix_banks import PixBanks
class PixUserDao:
    pg_admin: PostgresAdmin

    def __init__(self, pg_admin):
        self.pg_admin = pg_admin
    
    def create_pix_user(self, cuit, name, mail=None, phone=None):
        check_for_existing = self.find_pix_user_by_cuit(cuit)
        if check_for_existing is not None:
            return -1

        query = "INSERT INTO users(cuit, name"
        params = (cuit, name)
        if mail is not None:
            query += ", mail"
        if phone is not None:
            query += ", phone"
        query += ") VALUES(%s, %s"
        if mail is not None:
            query += ", %s"
            params += (mail,)
        if phone is not None:
            query += ", %s"
            params += (phone,)
        query += ")"
        check = self.pg_admin.query(query, params)
        return check

    def find_pix_user_by_cuit(self, cuit: str):
        query = "SELECT FROM users WHERE cuit = %s"
        params = (cuit,)
        result = self.pg_admin.select_query(query, params)
        if result == None or len(result) == 0:
            return -1
        return result[0]

    def add_bank_to_user_account(self, user_id:int, bank_id:int):
        query = "INSERT INTO user_to_banks(user_id, bank_id) VALUES(%d, %d)"
        params = (user_id, bank_id)
        check = self.pg_admin.query(query, params)
        return check
    
    def create_pix_bank_account(self, user_id:int, bank_id:int, cbu:str):
        if bank_id == 0: 
            result = get_galicia_user_dao().get_user_by_cbu(cbu)
        elif bank_id == 1:
            # STD (TODO: Change for new daos when created)
            result = get_galicia_user_dao().get_user_by_cbu(cbu)
        elif bank_id == 2:
            result = get_galicia_user_dao().get_user_by_cbu(cbu)
        if result is None:
            return -1
    
        # Chequee que existe esa cuenta en el banco
        query = "INSERT INTO bank_accounts(balance, bank_id, cbu) VALUES(%d, %d, %s)"
        params = (0, bank_id, cbu)
        result = self.pg_admin.query(query, params)
        if result is -1:
            return -1
        result = self.add_bank_to_user_account(user_id, bank_id)
        if result is -1:
            # self.pg_admin.remove_query(remover tupla insertada antes)
            return -1
        return 0
    
    def extract_from_account(self, bank_id:int, cbu:str):
        dao = self.get_user_dao_for_bank_id()
        if dao is None or dao.get_user_by_cbu(cbu) is None:
            return -1
        result = dao.extract_from_account(cbu)
        if result is None:
            return -1
        
        return 0
    
    def make_transaction(self, 
                         src_cbu:str, 
                         src_bank_code:str, 
                         dst_cbu:str,
                         dst_bank_code:str,
                         amount: int):
        """ Pasos:
        1) Tomar cuenta de banco de donde voy a extraer
            1.1) Chequear que esta cuenta exista en el banco indicado
        2) Chequear que esta cuenta tenga fondos
        3) Si tiene fondos, chequear que exista cuenta receptora en banco indicado
        4) Si ambas cuentas existen, y hay suficiente saldo,
        extraer de cuenta fuente (impactando en banco y en cuenta de banco en pix)
        y acreditar en la cuenta receptora (en pix y en banco)
        
        
        
        """
        dao = self.get_user_dao_for_bank_id(src_bank_code)
        sender = dao.get_user_by_cbu(src_cbu)
        if sender is None or sender.balance < amount:
            return (-1, "Sender not found or not enough funds")
        
        rcv_dao = self.get_user_dao_for_bank_id(dst_bank_code)
        receiver = dao.get_user_by_cbu(dst_cbu)
        if receiver is None:
            return (-1, "Receiver not found")
        
        t_dao = self.get_transfer_dao_for_bank_id(src_bank_code)
        transfer_id = t_dao.create_transfer(src_cbu, dst_cbu, 
                                         PixBanks.get_name_from_id(src_bank_code),
                                         PixBanks.get_name_from_id(dst_bank_code),
                                         amount)
        dao.transfer_to_account(transfer_id, src_cbu)
        dao.extract_from_account(src_cbu, amount)

        t_dao = self.get_transfer_dao_for_bank_id(dst_bank_code)
        transfer_id = t_dao.create_transfer(src_cbu, dst_cbu, 
                                         PixBanks.get_name_from_id(src_bank_code),
                                         PixBanks.get_name_from_id(dst_bank_code),
                                         amount)
        # Nota: Lo creo dos veces porque no puedo utilizar el mismo ID para ambas cosas
        rcv_dao.receive_transfer(transfer_id, dst_cbu)
        rcv_dao.deposit_to_account(dst_cbu, amount)

        # CREO QUE ESTO DEBERÍA FUNCIONAR

    def get_transfer_dao_for_bank_id(self, bank_id:int):
        if bank_id == 0: 
            return get_galicia_transfer_dao()
        elif bank_id == 1:
            # STD (TODO: Change for new daos when created)
            return None
            # return get_santander_user_dao()
        elif bank_id == 2:
            return None
            # return get_frances_user_dao()

    def get_user_dao_for_bank_id(self, bank_id:int):
        if bank_id == 0: 
            return get_galicia_user_dao()
        elif bank_id == 1:
            # STD (TODO: Change for new daos when created)
            return None
            # return get_santander_user_dao()
        elif bank_id == 2:
            return None
            # return get_frances_user_dao()