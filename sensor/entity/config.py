
from sensor.constants.training_pipeline import PIPELINE_NAME
from sensor.constants.training_pipeline import ARTIFACT_DIR
from datetime import datetime
import os
from sensor.constants.training_pipeline import *


class TrainingPipelineConfig:

    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name :str = PIPELINE_NAME
        self.artifacts_dir :str = os.path.join(ARTIFACT_DIR,timestamp)
        self.timestamp :str =  timestamp


class DataIngestionConfig:

    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        
        self.data_ingestion_dir: str = os.path.join(train_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME)

    
        self.feature_store_file_path: str = os.path.join(
        self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)


        self.training_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAINING_FILE)
        self.testing_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TESTING_FILE)
    
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME