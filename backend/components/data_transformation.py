import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from backend.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from backend.entity.config_entity import DataTransformationConfig
from backend.entity.artifact_entity import (
    DataTransformationArtifact,
    DataIngestionArtifact,
    DataValidationArtifact,
)
from backend.exception import MyException
from backend.logger import logging
from backend.utils.main_utils import save_object, save_csv_data, read_yaml_file
from collections import defaultdict
import re


class DataTransformation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e, sys) from e

    @staticmethod
    def read_data(file_path: str):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys) from e

    def get_data_transformer_object(self, df_columns) -> Pipeline:
        logging.info(
            "Entered get_data_transformed_object method of DataTransformation class"
        )
        try:

            logging.info("Cols loaded from schema")
            preprocessor = SentenceTransformer("all-MiniLM-L6-v2")  # Fast & effective

            column_embeddings = preprocessor.encode(df_columns, show_progress_bar=True)

            # Tune distance_threshold (try 1.0 to 1.5)
            clustering = AgglomerativeClustering(
                n_clusters=None,
                distance_threshold=0.5,
                metric="euclidean",
                linkage="ward",
            )
            cluster_labels = clustering.fit_predict(column_embeddings)

            cluster_map = defaultdict(list)
            for col, label in zip(df_columns, cluster_labels):
                cluster_map[label].append(col.strip())

            logging.info(
                "Exited get_data_transformer_object method of Data Tranformation class"
            )
            return cluster_map
        except Exception as e:
            raise MyException(e, sys) from e

    def _rename_columns(self, cluster_map, df):
        new_df = df.copy()
        logging.info("Renaming columns based on clustering")
        for label, cols in cluster_map.items():
            if len(cols) > 1:
                new_col_name = cols[0]  # Or any meaningful name
                new_df[new_col_name] = new_df[cols].max(axis=1)
                new_df.drop(columns=cols, inplace=True)
        logging.info("Columns renamed based on clustering")
        new_names = {col: re.sub(r"[^A-Za-z0-9_]+", "", col) for col in new_df.columns}
        new_n_list = list(new_names.values())
        # [LightGBM] Feature appears more than one time.
        new_names = {
            col: f"{new_col}_{i}" if new_col in new_n_list[:i] else new_col
            for i, (col, new_col) in enumerate(new_names.items())
        }
        new_df = new_df.rename(columns=new_names)
        return new_df

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Data Transformation started")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            train_df = self.read_data(
                file_path=self.data_ingestion_artifact.trained_file_path
            )
            test_df = self.read_data(
                file_path=self.data_ingestion_artifact.test_file_path
            )

            df_columns = list(train_df.columns)

            logging.info("Train and test data loaded")

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            logging.info("Input and Target Cols defined for both train and test df")

            logging.info("Custom transformation applied to test and train data")
            logging.info("Starting data Transformation!!")
            cluster_map = self.get_data_transformer_object(df_columns)
            logging.info("Data transformer object created. Starting renaming columns")
            transformed_train_df = self._rename_columns(
                cluster_map, input_feature_train_df
            )
            transformed_test_df = self._rename_columns(
                cluster_map, input_feature_test_df
            )
            logging.info("Renaming columns completed for train and test data")
            transformed_train_df[TARGET_COLUMN]=target_feature_train_df
            transformed_test_df[TARGET_COLUMN]=target_feature_test_df
            # logging.info("Initializing transformation fro training data")
            # input_feature_train_arr = cluster_map.fit_transform(transformed_train_df)
            # logging.info("Initializing transformation for testing data ")
            # input_feature_test_arr = cluster_map.transform(transformed_test_df)
            # logging.info("Transformation completed!!")
            # logging.info(input_feature_train_arr, input_feature_test_arr)

            # train_arr = np.c_[
            #     input_feature_train_arr, np.array(target_feature_train_df)
            # ]
            # test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            # logging.info("feature-target concatenation done for test-train df")

            # save_object(
            #     self.data_transformation_config.transformed_object_file_path,
            #     cluster_map,
            # )

            
            save_csv_data(
                self.data_transformation_config.transformed_train_file_path,
                file_csv=transformed_train_df,
            )
            save_csv_data(
                self.data_transformation_config.transformed_test_file_path,
                file_csv=transformed_test_df,
            )
            logging.info("Saving transformed object and transformed files")
            logging.info("Data Transformation completed!!")
            return DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

        except Exception as e:
            raise MyException(e, sys) from e
