
from sensor.constants.training_pipeline import *
from sensor.constants.training_pipeline import ARTIFACT_DIR
from datetime import datetime
import os
from sensor.constants.training_pipeline import *
from dataclasses import dataclass

@dataclass
class TrainingPipelineConfig:

    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name :str = PIPELINE_NAME
        self.artifacts_dir :str = os.path.join(ARTIFACT_DIR,timestamp)
        self.timestamp :str =  timestamp
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()



@dataclass
class DataIngestionConfig:

    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        
        self.data_ingestion_dir: str = os.path.join(train_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME)

    
        self.feature_store_file_path: str = os.path.join(
        self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)


        self.training_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAINING_FILE)
        self.testing_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TESTING_FILE)
    
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME

"""
class DataValidationConfiguration:
    
    def __init__(self,training_pipeline_config=TrainingPipelineConfig):
        
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifacts_dir,DATA_INGESTION_DIR_NAME)
        self.valid_data_dir:str = os.path.join(self.valid_data_dir,TRAINING_FILE)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, TRAINING_FILE)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, TESTING_FILE)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, TRAINING_FILE)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, TESTING_FILE)
        self.drift_report_file_path: str = os.path.join(self.data_validation_dir,  DATA_VALIDATION_DRIFT_REPORT_DIR,DATA_VALIDATION_DRIFT_REPORT_FILENAME)
 """
@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifacts_dir,DATA_VALIDATION_DIR_NAME)
    valid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_VALID_DIR)
    invalid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_INVALID_DIR)
    valid_training_file_path: str = os.path.join(valid_data_dir, TRAINING_FILE)
    valid_testing_file_path: str = os.path.join(valid_data_dir, TESTING_FILE)
    invalid_training_file_path: str = os.path.join(invalid_data_dir, TRAINING_FILE)
    invalid_testing_file_path: str = os.path.join(invalid_data_dir, TESTING_FILE)
    drift_report_file_path: str = os.path.join(data_validation_dir,DATA_VALIDATION_DRIFT_REPORT_DIR,DATA_VALIDATION_DRIFT_REPORT_FILENAME,)

@dataclass

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifacts_dir,DATA_TRANSFORMATION_DIR)

        self.transformed_training_file_path = os.path.join(self.data_transformation_dir,TRANSFORMED_DATA,TRAINING_FILE.replace("csv","npy"),)
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir,TRANSFORMED_DATA,TESTING_FILE.replace("csv","npy"),)
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,PREPROCESSING_FILE)

@dataclass
class ModelTrainerConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
    
        self.model_trainer_dir :str = os.path.join(training_pipeline_config.artifacts_dir,MODEL_TRAINER_DIR_NAME)
        self.trained__model_file_path:str = os.path.join(self.model_trainer_dir,MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_NAME)
        self.model_accuracy :float = EXPECTED_SCORE
        self.model_config_path : str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
@dataclass
class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.model_evaluation_dir :str = os.path.join(training_pipeline_config.artifacts_dir,MODEL_EVALUATION_DIR_NAME)

        self.report_file_path = os.path.join(self.model_evaluation_dir,MODEL_EVALUATION_REPORT_NAME)
        
        self.change_threshold =  MODEL_EVALUATION_THRESHOLD


@dataclass
class ModelPusherConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.model_evaluation_dir : str = os.path.join(training_pipeline_config.artifacts_dir,MODEL_PUSHER_DIR_NAME)
        timestamp = round(datetime.now().timestamp())
        self.saved_model_dir = os.path.join(SAVED_MODEL_DIR,f"{timestamp}",MODEL_NAME)
        self.model_file_path = os.path.join(self.model_evaluation_dir,MODEL_NAME)
