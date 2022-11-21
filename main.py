from sensor.connection_config.db_connection import MongoDBConnection
import os,sys
from sensor.entity.config import TrainingPipelineConfig,DataIngestionConfig
from sensor.pipeline.training import TrainingPipeLine

if __name__ == '__main__':

    training_pipeline = TrainingPipeLine()
    training_pipeline.Run_Pipeline()
   




'''
if __name__ == '__main__':

    try:
        mongodb_client = MongoDBConnection()
        print(mongodb_client.db.list_collection_names())
    except Exception as e:
        print(e)

'''