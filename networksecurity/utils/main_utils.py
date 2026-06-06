import os, sys, pickle
import yaml
from networksecurity import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from networksecurity.exceptions.exception import NetworkSecurityException
import numpy as np

# @ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content as ConfigBox.

    Args:
        path_to_yaml (Path): path to yaml file

    Raises:
        ValueError: if yaml file is empty
        NetworkSecurityException: if any error occurs

    Returns:
        ConfigBox: yaml content as ConfigBox
    """

    try:
        with open(path_to_yaml, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)

            if content is None:
                raise ValueError(f"YAML file is empty: {path_to_yaml}")

            logger.info(f"YAML file loaded successfully: {path_to_yaml}")

            return ConfigBox(content)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

# @ensure_annotations    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file.
    
    Args:
        file_path (str): The path where the YAML file will be saved.
        content (object): The content (dictionary/list) to write into the file.
        replace (bool): If True, replaces the file if it already exists.
    """
    try:
      
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
       
        with open(file_path, "w") as file:
            yaml.dump(content, file)
            
        logger.info(f"Successfully created YAML file at: {file_path}")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories(list): list of path directories
        ignore_log(bool, optional): ignore if multiple dirs is to be created. Defults to 
    """

    for path in path_to_directories:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_jason(path: Path, data: dict):
    """save json data

    Args:
        path (path): path to json file
        data(dict): data to save in json file
    """

    with open(path,"w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json data

    Args:
        path (path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file
     Args:
        path (path): path to binary file
        data(Any): data to save in binary file

    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved to {path}")



@ensure_annotations
def load_bin(path: Path):
    """load binary file
     Args:
        path (path): path to binary file
    Returns:
        Any: object stored in the file
    """

    data = joblib.load(path)
    logger.info(f"binary file loaded from {path}")
    return data



def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logger.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            logger.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

