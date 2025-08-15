from backend.logger import logging
from backend.exception import MyException
import sys
from backend.data_access.proj1_data import Proj1Data
from backend.constants import MODEL_BUCKET_NAME, DATASET_FILE_NAME
from backend.pipeline.training_pipeline import TrainPipeline

# try:
#     a=1+'z'
# except Exception as e:
#     logging.info(e)
#     raise MyException(e,sys) from e


# proj= Proj1Data()
# proj.export_collection_as_DataFrame(bucket_name=MODEL_BUCKET_NAME, file_name=DATASET_FILE_NAME)

t = TrainPipeline()
data_injestion_artifact = t.start_data_ingestion()
t.start_data_validation(data_injestion_artifact)
