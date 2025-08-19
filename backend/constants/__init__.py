import os 
from datetime import date

#Where you store your data


#Pipeline
PIPELINE_NAME: str=""
ARTIFACT_DIR: str="artifact"
MODEL_FILE_NAME="model.pkl"

TARGET_COLUMN= "diseases"
CURRENT_YEAR=date.today().year
PREPROCESSING_OBJECT_FILENAME="preprocessing.pkl"

FILE_NAME:str="data.csv"
TRAIN_FILE_NAME:str ="train.csv"
TEST_FILE_NAME:str="test.csv"
SCHEMA_FILE_PATH=os.path.join("config", "schema.yaml")

AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "ap-south-1"





#Data ingestion related constant start with DATA_INGESTION VAR NAME

DATA_INGESTION_COLLECTION_NAME:str="Proj1-Data"
DATA_INGESTION_DIR_NAME:str= "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str= "feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2

MODEL_BUCKET_NAME="mydataset111"
DATASET_FILE_NAME="new_merged_dataset.csv"
# DATASET_URL="https://mydataset11.s3.us-east-1.amazonaws.com"

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_REPORT_NAME:str="report.yaml"

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"