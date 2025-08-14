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