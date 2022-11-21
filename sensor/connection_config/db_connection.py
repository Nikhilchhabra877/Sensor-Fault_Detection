import pymongo
from sensor.constants.database import DATABASE_NAME
import certifi
from sensor.exception import CustomException
import os,sys
ca = certifi.where()


class MongoDBConnection:
    client = None
    def __init__(self, db_name = DATABASE_NAME) -> None:
        try:
            if MongoDBConnection.client is None:
                db_url = 'mongodb+srv://root:root@scaniatruck.3m5t41i.mongodb.net/?retryWrites=true&w=majority'
                MongoDBConnection.client = pymongo.MongoClient(db_url,tlsCAFile=ca)
            self.client = MongoDBConnection.client
            self.db = self.client[db_name]
            self.db_name = db_name
        except Exception as e:
            raise CustomException(e,sys)

