import sys,os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
    data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformaion_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_object(cls)->Pipeline:
        """
          It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
          and returns a Pipeline object with the KNNImputer object as the first step.

          Args:
            cls: DataTransformation
          Returns:
            A Pipeline object
        """
        logging.info("Entered get_data_trnasformer_object method of Trnasformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initlise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered iniate_data_transformation of DataTransformation class")
        try:
            logging.info("Starting Data Transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## training Dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            ## test Dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            preprocessor=self.get_data_transformer_object()

            preprocessor_obj=preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train_df=preprocessor_obj.transform(input_feature_train_df)
            transformed_input_feature_test_df=preprocessor_obj.transform(input_feature_test_df)


            train_arr =np.c_[transformed_input_feature_train_df,np.array(target_feature_train_df)]
            test_arr =np.c_[transformed_input_feature_test_df,np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformaion_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformaion_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformaion_config.transformed_object_file_path,preprocessor_obj)
            save_object("final_model/preprocessor.pkl",preprocessor_obj)

            #prepring artifact
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformaion_config.transformed_object_file_path,
                transformed_test_file_path=self.data_transformaion_config.transformed_test_file_path,
                transformed_train_file_path=self.data_transformaion_config.transformed_train_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)