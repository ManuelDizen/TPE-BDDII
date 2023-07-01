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

        with open('config/cbus.txt', 'r') as file:
            cbus = file.read().splitlines()
        cbu_galicia = cbus[0]
        cbu_santander = cbus[1]
        self.galicia_user_dao = GaliciaUserDao(self.db, int(cbu_galicia))

    def close_connection(self):
        self.client.close()
        with open('config/cbus.txt', 'w') as file:
            file.write(str(self.galicia_user_dao.get_base_cbu()) + '\n')
            file.write(str(0) + '\n') #TODO: Cuando tenga el de santander agregar acá
    
    def get_db(self):
        return self.db

    def get_galicia_user_dao(self):
        return self.galicia_user_dao