from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.components.data_transformation import DataTransformation

from networkSecurity.entity.config_entity import DataValidationConfig,DataTransformationConfig


from networkSecurity.components.model_trainer import ModelTrainer
from networkSecurity.entity.config_entity import ModelTrainerConfig

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
            logging.info("DataTransformation Started")
            data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
            
            data_transformation = DataTransformation(data_validation_artifact=datavalidationartifact,data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("DataTransformation Completed")
            
            print(data_transformation_artifact)
            
            logging.info("Model trainer started")
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            print(model_trainer_artifact)
            logging.info("Model trainer Ended")
            
    except Exception as e:
            raise NetworkSecurityException(e,sys)