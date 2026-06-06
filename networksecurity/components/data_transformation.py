from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS, TARGET_COLUMN
from networksecurity import logger
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils import *
import pandas as pd
import numpy as np
import os, sys

class DataTransformation:

    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
       try:
           self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
           self.data_transformation_config: DataTransformationConfig = data_transformation_config
       except Exception as e:
           raise NetworkSecurityException(e,sys)
       
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def get_data_transformer_object(cls) -> Pipeline:
        """
        
        """
        logger.info(
            "Entered get_data_transformer_object method of Transformation class"
        )
        try:
            
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            
            logger.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )

            
            processor: Pipeline = Pipeline([("imputer", imputer)])
            
            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    

    def initiate_data_transformation(self) -> DataValidationArtifact:
        logger.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logger.info("Starting data transformation")
                
                
            train_df = DataTransformation.read_data(self.data_validation_artifact.validation_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.validation_test_file_path)

             
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

                
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

               
            preprocessor = self.get_data_transformer_object()

            logger.info(f"Applying transformer object on training and testing dataframes")
                
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path, obj=preprocessor,)
            
            logger.info("Preprocessing object and transformed arrays saved successfully")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
                
        except Exception as e:
            raise NetworkSecurityException(e, sys)


