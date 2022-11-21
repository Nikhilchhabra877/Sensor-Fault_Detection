from sensor.entity.config import TrainingPipelineConfig,DataIngestionConfig
from sensor.exception import CustomException
import os,sys
from sensor.logger import logging
from sensor.entity.artifacts import DataIngestingArtifacts

class TrainingPipeLine:

    def __init__(self):

        training_pipeline =  TrainingPipelineConfig()
        self.data_ingestion = DataIngestionConfig(train_pipeline_config=training_pipeline)
        self.training_pipeline = training_pipeline


    def Data_Ingestion(self)->DataIngestingArtifacts:

        try:
            logging.info("staring data ingestion")
            logging.info("data ingestion completed successfully")
        except Exception as e:
            raise CustomException(e,sys)

    def Data_validation():

        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def Data_Transformation():

        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def Model_trainer():

        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def Model_evaluation():

        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def Model_Push():

        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def Run_Pipeline(self):

        try:
            data_ingestion_artifacts:DataIngestingArtifacts = self.Data_Ingestion()
        except Exception as e:
            raise CustomException(e,sys)



