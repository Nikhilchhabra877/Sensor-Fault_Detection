from sensor.connection_config.db_connection import MongoDBConnection
from sensor.entity.config import TrainingPipelineConfig,DataIngestionConfig
from sensor.pipeline.training import TrainingPipeLine
from sensor.exception import CustomException
import os,sys
from fastapi import FastAPI
from sensor.constants.application import HOST,PORT
from starlette.responses import RedirectResponse
from uvicorn import run  as app_run
from flask import Flask,Response
from sensor.constants.training_pipeline import *
from sensor.logger import logging
   
"""

if __name__ == '__main__':

    try:

        training_pipeline = TrainingPipeLine()
        training_pipeline.Run_Pipeline()
    except Exception as e:
        print(e)
        raise CustomException(e,sys)

"""

from sensor.MachineLearning.model.estimator import ModelReolver,TargetValueMapping
from sensor.utils.main_utils import load_object,read_yaml_file
from fastapi.middleware.cors import CORSMiddleware
import os

env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainingPipeLine()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.Run_Pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe

        df=None
        model_resolver = ModelReolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        set_env_variable(env_file_path)
        training_pipeline = TrainingPipeLine()
        training_pipeline.Run_Pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()
    # set_env_variable(env_file_path)
    app_run(app, host=HOST, port=PORT)