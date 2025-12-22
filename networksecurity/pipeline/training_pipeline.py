import os,sys

from networksecurity.cloud.s3_syncer import S3Sync
from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import *

from networksecurity.entity.artifact_entity import *


class TrainingPipeline:
    def __init__(self):
        self.training_pipline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(self.training_pipline_config)
            logging.info("Start Data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Completed and artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(self.training_pipline_config)
            logging.info("Start Data Validation")
            data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
            data_validation_artifact=data_validation.initate_data_validation()
            logging.info(f"Data Validation Completed and artifact:{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformtion(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(self.training_pipline_config)
            logging.info("Start Data Transformation")
            data_transformation= DataTransformation(data_validation_artifact,data_transformation_config)
            data_transformation_artifact=data_transformation.initate_data_transformation()
            logging.info(f"Data Transformation Completed and artifact:{data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config=ModelTrainerConfig(self.training_pipline_config)
            logging.info("Start Model Trainer")
            model_trainer=ModelTrainer(model_trainer_config,data_transformation_artifact)
            model_trainer_artifact= model_trainer.initiate_model_trainer()
            logging.info(f"Model trainer Completed and artifact:{model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformtion(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)



