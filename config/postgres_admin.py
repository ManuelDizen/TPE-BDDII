import psycopg2
from os import getenv

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

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        return result
