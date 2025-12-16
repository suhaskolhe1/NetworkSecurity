import yaml
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import os,sys,dill,pickle

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'r') as ymal_file:
            return yaml.safe_load(ymal_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    

def write_yaml_file(file_path:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)