from config.mongo_admin import MongoAdmin

mongo = MongoAdmin()

def get_galicia_user_dao():
    return mongo.get_galicia_user_dao()