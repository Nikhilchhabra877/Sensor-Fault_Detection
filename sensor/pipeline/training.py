from sensor.entity.config import TrainingPipelineConfig,DataIngestionConfig
from sensor.exception import CustomException
import os,sys
from sensor.logger import logging
from sensor.entity.artifacts import DataIngestingArtifacts
from sensor.stages.data_ingestion import DataIngestion

class TrainingPipeLine:

    def __init__(self):

        training_pipeline =  TrainingPipelineConfig()
        self.data_ingestion = DataIngestionConfig(train_pipeline_config=training_pipeline)
        self.training_pipeline = training_pipeline


    def Data_Ingestion(self)->DataIngestingArtifacts:

        try:
            logging.info("staring data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion)
            data_ingestion_artifacts =  data_ingestion.export_data_featurestore()
            logging.info(f"data ingestion completed successfully and artifacts: {data_ingestion_artifacts}")
            return data_ingestion_artifacts
            
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



