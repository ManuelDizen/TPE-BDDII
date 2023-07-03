from config.postgres_admin import PostgresAdmin

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
        self.pg_admin.insert_query(query, params)
        return 0

    def find_pix_user_by_cuit(self, cuit):
        query = "SELECT FROM users WHERE cuit = %s"
        params = (cuit,)
        result = self.pg_admin.select_query(query, params)
        if len(result) == 0:
            return None
        return result[0]

