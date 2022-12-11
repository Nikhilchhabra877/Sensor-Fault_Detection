import os, glob
from flask import Flask, render_template, redirect, flash, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from utils import *
import time
from datetime import datetime
import pandas as pd
from subprocess import call   



from sensor.connection_config.db_connection import MongoDBConnection
from sensor.entity.config import TrainingPipelineConfig,DataIngestionConfig
from sensor.pipeline.training import TrainingPipeLine
from sensor.exception import CustomException
import os,sys
from fastapi import FastAPI
from sensor.constants.application import HOST,PORT
from starlette.responses import RedirectResponse
from uvicorn import run  as app_run
from flask import Flask,Response,Request
from sensor.constants.training_pipeline import *
from sensor.logger import logging
import pandas as pd
import numpy as np
import shutil

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
from fastapi import File, UploadFile



app = Flask(__name__,static_url_path='/Static')
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER
app.config['ERROR_FOLDER'] = ERROR_FOLDER
app.config['SECRET_KEY'] = 'my secret'

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if not 'file' in request.files:
      flash('No file selected!')
      return redirect(request.url)

    file = request.files.get('file')
    if file.filename == '':
        flash('No file uploaded')
        return redirect(request.url)
    
    if file_valid(file.filename):
      filename = file.filename
      dateTimeObj = datetime.now().strftime("%y-%m-%d %H-%M-%S")
      filename = filename.split(".")
      filename = filename[0]+dateTimeObj+"."+filename[1]
      filename = secure_filename(filename)
      #print(filename)
      df = pd.read_csv(file)
      if df.shape[1] == 171:
        file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
        #call(["python3","main.py"])  # run main.py
        #time.sleep(10)
        #flash("Files uploaded successfully")
        df = df.replace(['na'], [np.NaN])
        df = df.drop(['br_000', 'bq_000', 'bp_000', 'ab_000', 'cr_000', 'bo_000', 'bn_000','class'],axis=1)
        model_resolver = ModelReolver(model_dir=SAVED_MODEL_DIR)
      
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred

        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        csv_file = df.to_csv('file_name.csv', encoding='utf-8')
       
        shutil.move('file_name.csv',f"Predictions/{filename}")
        return redirect(url_for('download'))
      else:
        flash("Number of features does not match. Please upload valid file")
        file.save(os.path.join(app.config['ERROR_FOLDER'], filename))
        return redirect(request.url)
    else:
      flash('Invalid file type')
      return redirect(request.url) 


@app.route("/download")
def download():

  # Get latest file from folder
  list_of_files = glob.glob(r'/Users/nikhil/project-SensorFaultDetection/Sensor-Fault_Detection/Predictions/*')
  latest_file = max(list_of_files, key = os.path.getctime)
  latest_file = os.path.basename(latest_file)
  #os.listdir('Predictions')
  return render_template('download.html',filename = latest_file)

@app.route("/download/<filename>")
def download_file(filename):
  return send_from_directory('Predictions',filename)


if __name__ == '__main__':
    app.run(debug=True)