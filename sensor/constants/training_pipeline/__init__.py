from sensor.constants.S3_bucket import TRAINING_BUCKET
import os


# constant variables for training pipeline

TARGET_NAME = "class"
PIPELINE_NAME : str = "sensor_model"
ARTIFACT_DIR :  str = "artifacts"
FILE_NAME : str = "sensor_data.csv"
TRAINING_FILE : str = "train.csv"
TESTING_FILE : str = "test.csv"

PREPROCESSING_FILE = "preprocessing.pkl"
MODEL_NAME = "sensor_model.pkl"
SCHEMA = os.path.join("config","schema.yaml")
SCHEMA_DROP_COLUMNS = "drop_columns"

# constant variables for data ingestion

DATA_INGESTION_COLLECTION_NAME: str = "sensor_fault_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

