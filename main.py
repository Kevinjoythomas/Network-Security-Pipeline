from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys
if __name__ == "__main__":
    
    try:    
            trainingpipelineconfig = TrainingPipelineConfig()
            dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
            dataingestion = DataIngestion(dataingestionconfig)
            logging.info("Initiate the data ingestion")
            
            dataingestionartifact = dataingestion.initiate_data_ingestion()
            print(dataingestionartifact)
    except Exception as e:
            raise NetworkSecurityException(e,sys)