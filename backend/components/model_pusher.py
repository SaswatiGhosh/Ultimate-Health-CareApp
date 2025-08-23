import sys
from backend.cloud_storage.aws_storage import SimpleStorageService
from backend.logger import logging
from backend.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from backend.exception import MyException
from backend.entity.config_entity import ModelPusherConfig
from backend.entity.s3_estimator import Proj1Estimator

class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact, model_pusher_config:ModelPusherConfig):
        self.mode_evaluation_artifact=model_evaluation_artifact
        self.model_pusher_config=model_pusher_config
        self.s3=SimpleStorageService()
        self.proj1_estimator=Proj1Estimator(bucket_name=model_pusher_config.bucket_name, model_path=self.model_pusher_config.s3_model_key_path)


    def initiate_model_pusher(self)->ModelPusherArtifact:
        logging.info("Entered initiate model_pusher method of ModelTrainer Class")
        try:
            print("........................................")
            logging.info("Uploading artifacts to s3 bucket")
            logging.info("Uploading new model to s3 bucket...")
            self.proj1_estimator.save_model(from_file=self.mode_evaluation_artifact.trained_model_path, remove=self.mode_evaluation_artifact.is_model_accepted)
            model_pusher_artifact=ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name, s3_model_path=self.model_pusher_config.s3_model_key_path)
            logging.info("Uploaded pusher Artifact:[{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")
            return model_pusher_artifact
        
        except Exception as e:
            raise MyException(e,sys) 
        