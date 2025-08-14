import sys,io
import pandas as pd
import numpy as np
from typing import Optional
from backend.logger import logging

from backend.configuration.aws_connection   import S3Client
from backend.constants import REGION_NAME

from backend.exception import MyException

class Proj1Data:
    def __init__(self) -> None:
        # print(DATABASE_NAME)
        try:
            self.s3client = S3Client(region_name=REGION_NAME).s3_client
            # print(self.s3client.)
        except Exception as e:
            raise MyException(e,sys)
        
    def export_collection_as_DataFrame(self, bucket_name :str , file_name:str) -> pd.DataFrame:

        try:
            if bucket_name is not None and file_name is not None:
                logging.info("Fetching Data from S3")
                response = self.s3client.get_object(Bucket=bucket_name, Key=file_name)
                logging.info("Fetching Data DONE from S3")
            data=io.BytesIO(response['Body'].read())
            df=pd.read_csv(data)
            logging.info(f" Data fetched with len : {len(df)}")
            return df
        except MyException as e:
            raise MyException(e,sys)
