from os import getenv

from pymongo import MongoClient
from pymongo.database import Database

from dao.galicia_user_dao import GaliciaUserDao

class MongoAdmin:
    client: MongoClient
    db: Database
    galicia_user_dao: GaliciaUserDao

    def start_connection(self):
        self.client = MongoClient(getenv("URL"))
        self.db = self.client["tpebddII"]
        self.galicia_user_dao = GaliciaUserDao(self.db)
    
    def close_connection(self):
        self.client.close()
    
    def get_db(self):
        return self.db

    def get_galicia_user_dao(self):
        return self.galicia_user_dao