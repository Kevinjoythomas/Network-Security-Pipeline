from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.entity.config_entity import DataValidationConfig
if __name__ == "__main__":
    
    try:    
            trainingpipelineconfig = TrainingPipelineConfig()
            dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
            dataingestion = DataIngestion(dataingestionconfig)
            logging.info("Initiate the data ingestion")
            
            dataingestionartifact = dataingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")
            
            print(dataingestionartifact)
            
            datavalidationconfig = DataValidationConfig(
                    training_pipeline_config=trainingpipelineconfig
                    )
            logging.info("Data Validation Initiated")
            
            datavalidation = DataValidation(
                    data_ingestion_artifact=dataingestionartifact,
                    data_validation_config=datavalidationconfig
                    )
            
            datavalidationartifact = datavalidation.initiate_data_validation()
            logging.info("Data Validation Completed")
            print(datavalidationartifact)
    except Exception as e:
            raise NetworkSecurityException(e,sys)