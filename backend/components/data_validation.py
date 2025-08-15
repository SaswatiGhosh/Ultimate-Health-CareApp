import json
import sys
import os
import pandas as pd
from pandas import DataFrame
from backend.exception import MyException
from backend.logger import logging
from backend.utils.main_utils import read_yaml_file
from backend.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from backend.constants import SCHEMA_FILE_PATH

# from backend.entity.config_entity import DataIngestionConfig, DataValidationConfig


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationArtifact,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        except Exception as e:
            raise MyException(e, sys) from e

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present:[{status}]")
            return status
        except Exception as e:
            raise MyException(e, sys) from e

    # removed the checking for catergorical and numerical columns

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_msg = ""
            logging.info("Starting Data validation")
            train_df, test_df = (
                DataValidation.read_data(
                    file_path=self.data_ingestion_artifact.trained_file_path
                ),
                DataValidation.read_data(
                    file_path=self.data_ingestion_artifact.test_file_path
                ),
            )

            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in Dataframe"
            else:
                logging.info(
                    f"All required columns present in traning dataframe: {status}"
                )

            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in Dataframe"
            else:
                logging.info(
                    f"All required columns present in testing  dataframe: {status}"
                )

            validation_status = len(validation_error_msg) == 0
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path,
            )

            report_dir = os.path.dirname(
                self.data_validation_config.validation_report_file_path
            )

            os.makedirs(report_dir, exist_ok=True)

            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_msg.strip(),
            }
            with open(
                self.data_validation_config.validation_report_file_path, "w"
            ) as report_file:
                json.dump(validation_report, report_file, indent=4)

            logging.info("Data validation artifact created and saved to JSON file")
            logging.info(f"Data validation atifact : {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise MyException(e, sys) from e
