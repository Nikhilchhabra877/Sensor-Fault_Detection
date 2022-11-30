from sensor.exception import CustomException
from sensor.logger import logging
import os,sys
from sensor.entity.config import DataIngestionConfig
from sensor.entity.artifacts import DataIngestingArtifacts
from pandas import DataFrame
from sensor.fetch_data.sensor_data import SensorData
from sensor.constants.database import DATABASE_NAME,COLLECTION_NAME
from sklearn.model_selection import train_test_split
from sensor.utils.main_utils import read_yaml_file
from sensor.constants.training_pipeline import SCHEMA

class DataIngestion:
    
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA)
        except Exception as e:
            raise CustomException(e, sys)
        
    def export_data_featurestore(self)->DataFrame:
        """
        Import data from MongoDB , record as DataFrame and store it into FeatureStore Directory
        """
        try:
            logging.info("Exporting data into FeatureStore")
            data_df = SensorData()
            dataframe  = data_df.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_path = self.data_ingestion_config.feature_store_file_path

            ## Now creating folders

            path = os.path.dirname(feature_store_path)
            os.makedirs(path,exist_ok=True)

            dataframe.to_csv(feature_store_path,index=False,header=True)

            return dataframe
        except Exception as e:
            raise CustomException(e,sys)


    def train_test_split(self,dataframe = DataFrame):


        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")
            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise CustomException(e, sys) from e


        """
        try:
            train_data,test_data = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Train-test Split started")
            logging.info("Initiate train_test split config from data ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting train and testing files path")
            train_data.to_csv(self.data_ingestion_config.training_file_path)
            test_data.to_csv(self.data_ingestion_config.testing_file_path)
            logging.info("Train test data exported successfully")
        except Exception as e:
            raise CustomException(e,sys)
        """
    

    def initiate_data_ingestion(self) -> DataIngestingArtifacts:

        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            dataframe = self.export_data_featurestore()
            dataframe = dataframe.drop(self._schema_config["drop_columns"],axis=1)
            #_schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            #dataframe = dataframe.drop(_schema_config["drop_columns"], axis=1)

            logging.info("Got the data from mongodb")

            self.train_test_split(dataframe)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestingArtifacts(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path,
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e

