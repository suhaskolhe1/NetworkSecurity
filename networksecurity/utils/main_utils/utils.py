from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
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


def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file:{file_path} does not exists!")
        with open(file_path,'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    


def save_object(file_path,obj:object):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(obj=obj,file=file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path:str)->np.array:
    """
    Load numpy array from file

    :param file_path: file location
    :type file_path: str
    :return: np.array
    :rtype: np.array
    """
    try:
        with open(file_path,'rb')as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report ={}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs = GridSearchCV(estimator=model,param_grid=para,cv=3,n_jobs=-1)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_train_pred=model.predict(X_train)

            y_test_pred=model.predict(X_test)

            train_model_score =r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        return report


    except Exception as e:
        raise NetworkSecurityException(e,sys)