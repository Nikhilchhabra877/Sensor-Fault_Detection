from sensor.exception import CustomException
from sensor.logger import logging
import os,sys
from sensor.entity.config import DataIngestionConfig
from sensor.entity.artifacts import DataIngestingArtifacts
from pandas import DataFrame
from sensor.fetch_data.sensor_data import SensorData
from sensor.constants.database import DATABASE_NAME,COLLECTION_NAME


class DataIngestion:
    def __init__(self,data_ingestion_config = DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config

    def export_data_featurestore(self)->DataFrame:
        """
        Import data from MongoDB , record as DataFrame and store it into FeatureStore Directory
        """
        try:
            logging.info("Exporting data into FeatureStore")
            data_df = SensorData()
            df  = data_df.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_path = self.data_ingestion_config.feature_store_file_path

            ## Now creating folders

            path = os.path.dirname(feature_store_path)
            os.makedirs(path,exist_ok=True)

            df.to_csv(feature_store_path,index=False,header=True)

            return df
        except Exception as e:
            raise CustomException(e,sys)


    def train_test_split(self,dataframe = DataFrame):

        pass

    def Data_Ingestion(self)->DataIngestingArtifacts:

        try:
            df = self.export_data_featurestore()
            self.train_test_split(dataframe=df)

            data_ingestion_artifacts = DataIngestingArtifacts(trained_file=self.data_ingestion_config.training_file_path,test_file=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifacts
        except Exception as e:
            raise CustomException(e,sys)
