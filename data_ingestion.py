import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
import certifi
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from dotenv import load_dotenv

load_dotenv()
ca = certifi.where()
MONGODB_URL = os.getenv("MONGO_DB_URL")


class NetworkDataIngestion():
    def __init__(self) -> None:
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path).reset_index(drop = True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def pushing_data_to_mongodb(self,records,database,collection):
        try:
            self.database_name = database
            self.collection_name = collection
            self.records = records
            self.client = pymongo.MongoClient(MONGODB_URL)
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            self.collection.insert_many(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
if __name__ == "__main__":
    File_Path = "D:/MLOPS/NETWORK_SECURITY/data/NetworkData.csv"
    DATABASE = "MLOPS"
    COLLECTION = "NetworkData"
    NDI = NetworkDataIngestion()  
    records = NDI.csv_to_json_converter(File_Path)
    noof_records = NDI.pushing_data_to_mongodb(records,DATABASE,COLLECTION)
    # print(noof_records)
