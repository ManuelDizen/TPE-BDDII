import psycopg2
from os import getenv
from dao.pix_user_dao import PixUserDao
# sudo docker run --name tpebdd2 -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres (Para correr el postgres local con docker)

class PostgresAdmin:
    connection = None
    cursor = None
    pix_user_dao: PixUserDao

    def start_connection(self):
        self.connection = psycopg2.connect(database=getenv("PG_DB_NAME"),
                                host=getenv("PG_BD_HOST"),
                                user=getenv("PG_USERNAME"),
                                password=getenv("PG_PASSWORD"),
                                port=getenv("PG_PORT"))
        self.cursor = self.connection.cursor()
        with open("config/table_creation_pix.sql", 'r') as sql_file:
            # Execute the script
            self.cursor.execute(sql_file.read())
            self.connection.commit()
        self.pix_user_dao = PixUserDao(self.connection, self.cursor)
    
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        
    def get_pix_user_dao(self):
        return self.pix_user_dao