from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys
from dotenv import load_dotenv
import os
import json
import certifi

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def cv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index()
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database =database
            self.collection  =collection
            self.records = records
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            self.database = self.mongo_client[self.database]
            
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len((self.records)))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
if __name__ == "__main__":
    FILE_PATH = "./Network_Data/phisingData.csv"
    DATABASE = "KEVIN"
    Collection  = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_json_converter(file_path=FILE_PATH)
    # print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    
    print(no_of_records)