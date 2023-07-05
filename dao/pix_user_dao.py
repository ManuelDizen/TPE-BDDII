import psycopg2
from models.pix_banks import PixBanks
class PixUserDao:
    connection = None
    cursor = None

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_from_cuit(self, cuit:str):
        query = "SELECT * FROM users WHERE cuit = %s"
        params = (cuit,)
        result = self.select_query(query,params)
        if result is None or len(result) == 0:
            return -1
        return result[0]
    
    def create_pix_user(self, cuit, name, mail=None, phone=None):
        check_for_existing = self.find_pix_user_by_cuit(cuit)
        if check_for_existing != -1:
            return -1

        query = "INSERT INTO users(cuit, name"
        params = (cuit, name)
        if mail is not None:
            query += ", email"
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
        check = self.query(query, params)
        return check

    def find_pix_user_by_cuit(self, cuit: str):
        query = "SELECT FROM users WHERE cuit = %s"
        params = (cuit,)
        result = self.select_query(query, params)
        if result == None or len(result) == 0:
            return -1
        return result[0]

    def add_bank_to_user_account(self, user_id:int, bank_id:int):
        print(str(user_id))
        print(str(bank_id))
        query = "INSERT INTO user_to_banks(user_id, bank_id) VALUES (%s, %s)"
        params = (user_id, bank_id)
        print(params)
        check = self.query(query, params)
        return check
    
    def create_pix_bank_account(self, user_cuit:int, bank_id:int, cbu:str):    
        # Chequee que existe esa cuenta en el banco
        print("Entro a primer query")
        query = "INSERT INTO bank_accounts(balance, bank_id, cbu) VALUES(%s, %s, %s)"
        params = (str(0), str(bank_id), cbu)
        result = self.query(query, params)
        if result == -1:
            print("El query salió mal")
            return -1
        user = self.select_query("SELECT * FROM users WHERE cuit = %s", (user_cuit,))
        print(user)
        result = self.add_bank_to_user_account(user[0][0], bank_id)
        if result == -1:
            # self.remove_query(remover tupla insertada antes)
            return -1
        return 0
    
    def extract_from_account(self, bank_id:int, cbu:str, amount:int):
        query = "SELECT * FROM bank_accounts WHERE bank_id = %s AND cbu = %s"
        params = (bank_id, cbu)
        user = self.select_query(query, params)
        if user is None or len(user) == 0:
            return -1
        user_balance = user[1] # id, balance, bank_id, cbu
        print(user)
        print(user_balance)

        query = "UPDATE bank_accounts SET balance = %s WHERE bank_id = %s AND cbu = %s"
        params = (int(user_balance) - amount, bank_id, cbu)
        self.query(query, params)
        return 0
    
    def add_to_account(self, bank_id:int, cbu:str, amount:int):
        query = "SELECT * FROM bank_accounts WHERE bank_id = %s AND cbu = %s"
        params = (bank_id, cbu)
        user = self.select_query(query, params)
        if user is None or len(user) == 0:
            return -1
        user_balance = user[1] # id, balance, bank_id, cbu
        print(user)
        print(user_balance)

        query = "UPDATE bank_accounts SET balance = %s WHERE bank_id = %s AND cbu = %s"
        params = (int(user_balance) + amount, bank_id, cbu)
        self.query(query, params)
        return 0

    def select_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except psycopg2.Error as e:
            return None
        
    def query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return 0
        except psycopg2.Error as e:
            print(e)
            return -1