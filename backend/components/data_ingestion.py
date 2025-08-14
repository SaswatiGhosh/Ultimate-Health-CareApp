import sys, os
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from backend.entity.config_entity import DataIngestionConfig
from backend.entity.artifact_entity import DataIngestionArtifact
from backend.constants import DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
from backend.exception import MyException
from backend.logger import logging
from backend.data_access.proj1_data import Proj1Data

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig= DataIngestionConfig()):
        try:
            self.data_ingestion_config= data_ingestion_config
        except MyException as e:
            raise MyException(e,sys)
        
    def export_data_into_feature_store(self)->DataFrame:
        try:
            logging.info(f"Exporting data from s3")
            my_data=Proj1Data() #
            dataframe=my_data.export_collection_as_DataFrame(bucket_name=self.data_ingestion_config.bucket_name,file_name=self.data_ingestion_config.file_name)
            logging.info(f"Dataframe created with shape {dataframe.shape}")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving Exported data into feature_store file path {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False)
            return dataframe
        except MyException as e:
            raise MyException(e,sys)
    
    def split_data_as_train_test(self,dataframe:DataFrame) -> None:
        logging.info("Entered train test _data_as_train method of Data Ingestion Class")
        try:
            train_set, test_set = train_test_split(dataframe, test_size=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO)
            logging.info(f"Splitting data into train and test set on the Dataframe")
            logging.info("Exited split data as train test method of DataIngestion Class")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False , header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False , header=True)
            logging.info(f"Exported test and train file path")
        except MyException as e:
            raise MyException(e,sys)
        
    def initiate_data_ingestion(self):
        logging.info("Entered initiate_data_ingestion method of Data Ingestion Class")
        try:
            dataframe= self.export_data_into_feature_store()
            logging.info("Got the data from ")
            self.split_data_as_train_test(dataframe)
            logging.info("Exited initiate data ingestion method of DataIngestion Class")
            data_ingestion_artifact= DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f"Data ingestion artifact created")
            return data_ingestion_artifact
        

        except Exception as e:
            raise MyException(e,sys)
