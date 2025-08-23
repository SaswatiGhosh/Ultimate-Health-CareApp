
from backend.entity.config_entity import ModelEvaluationConfig
from backend.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from backend.constants import TARGET_COLUMN
from backend.exception import MyException
from backend.logger import logging
from backend.utils.main_utils import load_object
import sys
import pandas as pd
from typing import Optional
from backend.entity.s3_estimator import Proj1Estimator
from dataclasses import dataclass
import re
@dataclass
class ModelEvaluationResposne:
    trained_mode_f1_score:float
    best_model_f1_score:float
    is_model_accepted:bool
    difference:float


class ModelEvaluation:
    def __init__(self, model_evaluation_config:ModelEvaluationConfig, data_ingestion_artifact:DataIngestionArtifact, model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_evaluation_config=model_evaluation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def get_best_model(self)->Optional[Proj1Estimator]:
        try:
            bucket_name=self.model_evaluation_config.bucket_name
            model_path=self.model_evaluation_config.s3_model_key_path
            proj1_estimator=Proj1Estimator(bucket_name=bucket_name, model_path=model_path)
            if proj1_estimator.is_model_present(model_path=model_path):
                return proj1_estimator
            return None
        except Exception as e:
            raise MyException(e,sys) from e
        
    # def _rename_columns(self, cluster_map, df):
    #     new_df = df.copy()
    #     logging.info("Renaming columns based on clustering")
    #     for label, cols in cluster_map.items():
    #         if len(cols) > 1:
    #             new_col_name = cols[0]  # Or any meaningful name
    #             new_df[new_col_name] = new_df[cols].max(axis=1)
    #             new_df.drop(columns=cols, inplace=True)
    #     logging.info("Columns renamed based on clustering")
    #     new_names = {col: re.sub(r"[^A-Za-z0-9_]+", "", col) for col in new_df.columns}
    #     new_n_list = list(new_names.values())
    #     # [LightGBM] Feature appears more than one time.
    #     new_names = {
    #         col: f"{new_col}_{i}" if new_col in new_n_list[:i] else new_col
    #         for i, (col, new_col) in enumerate(new_names.items())
    #     }
    #     new_df = new_df.rename(columns=new_names)
    #     return new_df

    def evaluate_model(self):
        try:
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x,y=test_df(TARGET_COLUMN,axis=1), test_df[TARGET_COLUMN]

            logging.info("Test data loaded and now transforming it for Prediction")
            # x=self._rename_columns(x)

            print(x)
            trained_model=load_object(file_path=self.model_trainer_artifact.trained_model_file_path)
            logging.info("Training model loaded/exist")

            trained_model_f1_score=self.model_trainer_artifact.metric_artifact.f1_score
            logging.info(f"f1_score for this model: {trained_model_f1_score}")
            best_model_f1_score=None
            best_model=self.get_best_model()
            if best_model is not None:
                logging.info("Best model_loaded/exist")
                y_hat_best_model=best_model.predict(x)
                best_model_f1_score=f1_score(y,y_hat_best_model)
                logging.info(f"f1_score for best_model :{best_model_f1_score}, f1_score-New trained Model : {trained_model_f1_score}")
            temp_best_model=0 if best_model_f1_score is None else best_model_f1_score

            result= ModelEvaluationResposne(trained_mode_f1_score=trained_model_f1_score, best_model_f1_score=best_model_f1_score,is_model_accepted=trained_model_f1_score>temp_best_model,difference=trained_model_f1_score-temp_best_model)
            logging.info(f"Result:{result}")
            return result
        except Exception as e:
            raise MyException(e,sys)
        
    def initiate_model_evaluation(self):
        try:
            print(".......................................")
            logging.info("Model evaluation initiated")
            evaluate_model_response=self.evaluate_model()
            s3_model_path=self.model_evaluation_config.bucket_name
            model_evaluation_artifact= ModelEvaluationArtifact(is_model_accepted=evaluate_model_response.is_model_accepted,
                                                              s3_model_path=s3_model_path,
                                                              trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                                                              changed_accuracy=evaluate_model_response.difference)
            logging.info(f"Model evaluation completed: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys)
        
