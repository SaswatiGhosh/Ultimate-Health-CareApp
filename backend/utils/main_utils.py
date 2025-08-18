import os
import sys
import yaml
import numpy as np
import pandas as pd
import dill
from sklearn.pipeline import Pipeline

from backend.exception import MyException
from backend.logger import logging

def read_yaml_file(file_path:str):
    try:
        with open(file_path,'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except MyException as e:
        raise MyException(sys,e)
    


def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb" ) as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise MyException(e,sys) from e
    

def load_numpy_array_data(file_path:str) ->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MyException(sys,e)


def save_object(file_path:str, obj:object) ->None:
    logging.info("Entered the save object method of utils")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    
        logging.info("Exited the save object method of utils")
    except Exception as e:
        raise MyException(e,sys) from e
    
