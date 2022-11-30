from sensor.exception import CustomException
import yaml
import os,sys
import numpy as np
import dill
from sensor.logger import logging

def read_yaml_file(file_path:str) -> dict:

    try:
        with open(file_path,'rb') as yaml_file:
           return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(file_path: str , content:object, replace:bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)

def save_numpy_array(file_path:str,array:np.array):
    """
    This function save the numpy array to a fle
    """

    try:
        
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as np_obj:
            np.save(np_obj,array)
    
    except Exception as e:
        raise CustomException(e,sys)


def load_numpy_array(file_path:str)->np.array:

    """
    This function load numpy array data from file
    """

    try:

        with open(file_path,"rb") as np_obj:
            np.load(np_obj,)
    except Exception as e:
        raise CustomException(e,sys)
    

def save_object(file_path:str,obj:object)->None:
    try:
    
        logging.info("Save object method invoked")
        os.makedirs(os.path.dirname(file_path),exist_ok = True)
        with open(file_path, "wb") as np_obj:
            dill.dump(obj,np_obj)
        logging.info(f"Object saved into the directory")


    except Exception as e:
        raise CustomException(e,sys)
    


def load_object(file_path:str)->object:

    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file is not available at {file_path}")
        
        with open (file_path,"wb") as obj:
            dill.load(obj)
            return dill

    except Exception as e:
        raise CustomException(e,sys)