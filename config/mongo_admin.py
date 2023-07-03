from os import getenv

from pymongo import MongoClient
from pymongo.database import Database

from dao.galicia_user_dao import GaliciaUserDao
from dao.galicia_transfer_dao import GaliciaTransferDao
from dao.santander_transfer_dao import SantanderTransferDao
from dao.santander_user_dao import SantanderUserDao

class MongoAdmin:
    client: MongoClient
    db: Database
    galicia_user_dao: GaliciaUserDao
    galicia_transfer_dao: GaliciaTransferDao
    santander_user_dao: SantanderUserDao
    santander_transfer_dao: SantanderTransferDao

    def start_connection(self):
        self.client = MongoClient(getenv("URL"))
        self.db = self.client["tpebddII"]

        with open('config/cbus.txt', 'r') as file:
            cbus = file.read().splitlines()
        cbu_galicia = cbus[0]
        cbu_santander = cbus[1]

        self.galicia_transfer_dao = GaliciaTransferDao(self.db)
        self.galicia_user_dao = GaliciaUserDao(self.db, int(cbu_galicia))
        self.santander_transfer_dao = SantanderTransferDao(self.db)
        self.santander_user_dao = SantanderUserDao(self.db, int(cbu_santander))

    def close_connection(self):
        self.client.close()
        with open('config/cbus.txt', 'w') as file:
            file.write(str(self.galicia_user_dao.get_base_cbu()) + '\n')
            file.write(str(self.santander_user_dao.get_base_cbu()) + '\n') #TODO: Cuando tenga el de santander agregar acá
    
    def get_db(self):
        return self.db

    def get_galicia_user_dao(self):
        return self.galicia_user_dao
    
    def get_galicia_transfer_dao(self):
        return self.galicia_transfer_dao
    
    def get_santander_user_dao(self):
        return self.santander_user_dao
    
    def get_santander_transfer_dao(self):
        return self.santander_transfer_dao