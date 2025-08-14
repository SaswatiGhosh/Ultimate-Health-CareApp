import sys
from backend.exception import MyException
from backend.logger import logging

from backend.components.data_ingestion import DataIngestion





from backend.entity.config_entity import DataIngestionConfig


from backend.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config= DataIngestionConfig()

    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            logging.info("Entered the start_data_ingestion of TrainPipeline class")
            logging.info("Getting the data from S3")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got train and test set from S3 bucket")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except MyException as e:
            raise MyException(e,sys)
