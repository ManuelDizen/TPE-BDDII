import psycopg2
from os import getenv

# sudo docker run --name tpebdd2 -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres (Para correr el postgres local con docker)

class PostgresAdmin:
    connection = None
    cursor = None

    def start_connection(self):
        self.connection = psycopg2.connect(database=getenv("PG_DB_NAME"),
                                host=getenv("PG_BD_HOST"),
                                user=getenv("PG_USERNAME"),
                                password=getenv("PG_PASSWORD"),
                                port=getenv("PG_PORT"))
        self.cursor = self.connection.cursor()
        print("Postgres connection started.")
    
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("Postgres connection ended")

    def select_query(self, query, params=None):
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        return result
    
    def insert_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()