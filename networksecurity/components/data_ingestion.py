import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split


load_dotenv()
ca = certifi.where()
MONGODB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config=data_ingestion_config
            self.feature_store_filepath = self.data_ingestion_config.feature_store_file_path
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_collection_as_dataframe(self):
        try:
            self.database_name = self.data_ingestion_config.database_name
            self.collection_name = self.data_ingestion_config.collection_name
            self.client = pymongo.MongoClient(MONGODB_URL)
            self.collection = self.client[self.database_name][self.collection_name]
            data = pd.DataFrame(list(self.collection.find()))
            if "_id" in data.columns:
                data = data.drop(columns=["_id"])
            data = data.replace({"na":np.nan})   
            return data 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_data_into_featurestore(self,data: pd.DataFrame):
        try:
            dir_name = os.path.dirname(self.feature_store_filepath)
            os.makedirs(dir_name,exist_ok=True)
            data.to_csv(self.feature_store_filepath,index=False,header=True)
            return data
        except Exception as e:
            raise NetworkSecurityException(e,sys)   
    def split_data_as_train_test(self,data: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                data, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)   
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            logging.info("Reading Data from MongoDB")
            dataframe = self.export_data_into_featurestore(dataframe)
            logging.info("Writing data in Feature Store")
            self.split_data_as_train_test(data=dataframe)
            logging.info("Train - Test Splitting")
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            
            return data_ingestion_artifact    
        except Exception as e:
            raise NetworkSecurityException(e,sys)            
            
            