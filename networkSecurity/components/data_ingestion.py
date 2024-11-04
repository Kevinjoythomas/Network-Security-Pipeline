from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging


from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.artifact import DataIngestionArtifact
import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo
import pandas as pd
from typing import List
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_collection(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            # print(df.head())
            if "_id" in df.columns.to_list():
               df.drop('_id',axis=1,inplace=True)
            # if df.empty:
            #     print("DataFrame is empty. No records found in the collection.")
        
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)        
    def export_data_into_fs(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try: 
            if dataframe.empty:
                raise ValueError("The input DataFrame is empty. Please check the data loading process.")
            train_set,test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on dataframe")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting train and test file path")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True
            )
            
            logging.info("Exported train and test csv completed")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)        
    def initiate_data_ingestion(self):
        try:
            df =  self.export_collection()
            df = self.export_data_into_fs(df)
            self.split_data_as_train_test(df)
            dataingestionartifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)