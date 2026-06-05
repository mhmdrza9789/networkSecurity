import os
import sys
import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity import logger
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_to_feature_store(self) -> pd.DataFrame:
        """
        Method Name: export_data_to_feature_store
        Description: This method reads data from SQLite and exports it to the feature store.
        """
        try:
            logger.info("Extracting data from SQLite database")
            
            db_path = self.data_ingestion_config.database_name
            table_name = self.data_ingestion_config.table_name
            
            # Connect to SQLite and fetch data
            with sqlite3.connect(db_path) as conn:
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            
            logger.info(f"Data shape from DB: {df.shape}")

            # Cleaning logic: handle MongoDB artifacts and nulls
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            # Create directory and save to feature store
            feature_store_file_path = self.data_ingestion_config.feature_store_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            
            logger.info(f"Saving raw data to: {feature_store_file_path}")
            df.to_csv(feature_store_file_path, index=False, header=True)
            
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def split_data_as_train_test(self, df: pd.DataFrame):
        """
        Method Name: split_data_as_train_test
        Description: This method splits the dataframe into train and test sets.
        """
        try:
            logger.info("Starting train-test split")
            
            train_set, test_set = train_test_split(
                df, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            # Create directory for ingested data
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logger.info(f"Exporting train/test files to {dir_path}")

            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

            logger.info("Train and test files saved successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        train_set, test_set = train_test_split(
            dataframe, test_size= self.data_ingestion_config.train_test_split_ratio
        )

        logger.info("performed train test split on dataframe")

        dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
        os.makedirs(dir_path, exist_ok=True)

        logger.info(f"Exporting train and test file path")

        train_set.to_csv(
            self.data_ingestion_config.train_file_path, index=False, header=True
        )

        test_set.to_csv(
            self.data_ingestion_config.test_file_path, index=False, header=True
        )

    def initiate_data_ingestion(self) :
        """
        Method Name: initiate_data_ingestion
        Description: Orchestrates the entire data ingestion process.
        """
        try:
            logger.info("Initiating Data Ingestion component")
            
            dataframe = self.export_data_to_feature_store()
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path,
                                                             test_file_path=self.data_ingestion_config.test_file_path)

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
