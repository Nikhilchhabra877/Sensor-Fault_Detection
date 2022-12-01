from sensor.constants.S3_bucket import TRAINING_BUCKET
import os

SAVED_MODEL_DIR= os.path.join("saved_models")

# constant variables for training pipeline

TARGET_NAME = "class"
PIPELINE_NAME : str = "sensor_model"
ARTIFACT_DIR :  str = "artifacts"
FILE_NAME : str = "sensor_data.csv"
TRAINING_FILE : str = "train.csv"
TESTING_FILE : str = "test.csv"

PREPROCESSING_FILE = "preprocessing.pkl"
#MODEL_NAME = "sensor_model.pkl"
SCHEMA = os.path.join("config","schema.yaml")
SCHEMA_DROP_COLUMNS = "drop_columns"

# constant variables for data ingestion

DATA_INGESTION_COLLECTION_NAME: str = "sensor_fault_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2


# constant variables for data validation

DATA_VALIDATION_DIR_NAME =  "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILENAME = "report.yaml"

# data transformation constants

DATA_TRANSFORMATION_DIR = "data_transformation"
TRANSFORMED_DATA = "data_transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

# Model trainer constants

MODEL_TRAINER_DIR_NAME :str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_NAME :str= "model.pkl"
EXPECTED_SCORE :float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")


# Model evaluation

MODEL_EVALUATION_THRESHOLD : float = 0.02
MODEL_EVALUATION_DIR_NAME:str = "model_trainer"
MODEL_EVALUATION_REPORT_NAME  = "report.yaml"

#Model Pusher

MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR
