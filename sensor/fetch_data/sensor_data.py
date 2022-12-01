import sys,os
from sensor.connection_config.db_connection import MongoDBConnection
from sensor.constants.database import DATABASE_NAME,COLLECTION_NAME
from sensor.exception import CustomException
import pandas as pd
import numpy as np
from typing import Optional
from sensor.logger import logging

class FetchSensorData:

    """
    This class will fetch the data from MONGODB and convert that into DataFrame
    """

    def __init__(self):
        try:
            self.mongodbclient = MongoDBConnection(db_name = DATABASE_NAME)
            
        except Exception as e:
            raise CustomException(e,sys)

"""  
    def export_collection_as_df(self,collection_name:str,db_name:Optional[str]=None) -> pd.DataFrame:

        try:
            if db_name is None:
               collection_name = self.mongodbclient.db[COLLECTION_NAME]
            else:

                collection_name = self.mongodbclient[db_name][COLLECTION_NAME]

                

                df = pd.DataFrame(list(collection_name.find()))
                if "_id" in df.columns.to_list():
                        df = df.drop(columns=["_id"], axis=1)
                df.replace({"na": np.nan}, inplace=True)
                return collection_name


        except Exception as e:
            raise CustomException(e,sys)

"""


class SensorData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        """
        """
        try:
            logging.info("Connection with MongoDB established successfully")
            self.mongo_client = MongoDBConnection(db_name=DATABASE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

    def export_collection_as_dataframe(
        self, collection_name: str, db_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            logging.info("data extraction started")
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection
            """
            if db_name is None:
                collection = self.mongo_client.db[collection_name]
            else:
                collection = self.mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            logging.info("Data Extracted successfully")
            return df
        except Exception as e:
            raise CustomException(e, sys)


