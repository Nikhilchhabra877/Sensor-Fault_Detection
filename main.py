from sensor.connection_config.db_connection import MongoDBConnection
from sensor.entity.config import TrainingPipelineConfig,DataIngestionConfig
from sensor.pipeline.training import TrainingPipeLine
import os,sys
   


if __name__ == '__main__':

    training_pipeline = TrainingPipeLine()
    training_pipeline.Run_Pipeline()
   

