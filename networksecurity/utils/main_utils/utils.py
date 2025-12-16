
import yaml
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import os,sys,dill,pickle
import numpy as np

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

def save_numpy_array_data(file_path:str,array:np.array):
    """
    Docstring for save_numpy_array_data
    
    :param file_path: str location of file to save
    :type file_path: str
    :param array: np.array data to save
    :type array: np.array
    """
    try:
        dir_path =os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_object(file_path,obj:object):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(obj=obj,file=file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)