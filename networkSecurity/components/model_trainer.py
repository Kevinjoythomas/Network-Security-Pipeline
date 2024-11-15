import pandas as pd
import os,sys

from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

from networkSecurity.entity.artifact import DataTransformationArtifact,ModelTrainer_Artifact
from networkSecurity.entity.config_entity import ModelTrainerConfig

from networkSecurity.utils.ml_utils.model.estimator import NetworkModel
from networkSecurity.utils.main_utils.utils import save_obj, load_object
from networkSecurity.utils.main_utils.utils import save_numpy,load_numpy

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from networkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networkSecurity.utils.main_utils.utils import evaluate_models
import mlflow
from urllib.parse import urlparse

import dagshub
# dagshub.init(repo_owner='kevinjoythomas2004', repo_name='Network-Security-Pipeline', mlflow=True)
os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/kevinjoythomas2004/Network-Security-Pipeline.mlflow"

class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig,data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:    
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self, best_model, classificationmetric):
            mlflow.set_registry_uri("https://dagshub.com/kevinjoythomas2004/Network-Security-Pipeline.mlflow")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            
            # Start the MLflow run
            with mlflow.start_run():
                f1_score = classificationmetric.f1_score
                precision_score = classificationmetric.precision_score
                recall_score = classificationmetric.recall_score
                
                # Append "train_" or "test_" to distinguish between training and testing metrics
                mlflow.log_metric(f"f1_score", f1_score)
                mlflow.log_metric(f"recall_score", recall_score)
                mlflow.log_metric(f"precision_score", precision_score)
                
                # Log the model
                if tracking_url_type_store != "file":
                    # Register the model in case of a remote tracking server
                    mlflow.sklearn.log_model(best_model, "model", registered_model_name="network_security_model")
                else:
                    # Log the model without registering it if it's local
                    mlflow.sklearn.log_model(best_model, "model")
                    
    def train_model(self,X_train, y_train,X_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
            }
            
            model_report:dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)
            
            best_model_score = max(sorted(model_report.values()))
            
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)
            
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)
            
            
            self.track_mlflow(best_model,classification_train_metric)
            
            self.track_mlflow(best_model,classification_test_metric)
                        
            
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            
            os.makedirs(model_dir_path,exist_ok=True)
            
            network_model = NetworkModel(preprocessor=preprocessor,model=best_model)
            save_obj(self.model_trainer_config.trained_model_file_path,obj=network_model)
            
            save_obj("final_model/model.pkl",best_model)
            model_trainer_artifact = ModelTrainer_Artifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                  train_metric_artifact=classification_train_metric,
                                  test_metric_artifact=classification_test_metric)
            
            logging.info(f"MODEL TRAINER ARTIFACT \n {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e: 
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainer_Artifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy(train_file_path)
            test_arr = load_numpy(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
                   
            )
            
            model_trainer_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)