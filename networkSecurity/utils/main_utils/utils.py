
import yaml
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:  
        raise NetworkSecurityException(e,sys) from e
    
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb" ) as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
    
def save_obj(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Existed the save Object Method of MainUtils")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e 