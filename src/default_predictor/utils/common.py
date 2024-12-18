import os
from box.exceptions import BoxValueError
import yaml
from default_predictor import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import pandas as pd


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read YAML files and returns
    
    Args:
        path_to_yaml (str): path of the YAML file
        
    Raises:
        ValueError: If the YAML file is empty
        e: empty file
        
    Returns:
        ConfigBox: ConfigBox type file
    """
    
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {path_to_yaml} loaded successfuly")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Create a list of directories
    
    Args:
        path_to_directories (list): A list of path to directories
        
    """
    
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at {path}")
            
@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save the JSON file
    
    Args:
        path (Path): Path of the JSON file
        data (Dict): Data to tbe saved in JSON
        
    """
    
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
        
    logger.info(f"JSON file saved at {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load the JSON files
    
    Args:
        path (Path): Path to the JSON file
        
    Returns:
        Configbox: Data as class attributes instead of dictionary
    
    """
    
    with open(path) as f:
        content=json.load(f)
        
    logger.info(f"JSON file loaded succesfully from {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save the binary files
    
    Args:
        data (Any): Data to be saved as binary file
        path (Path): Path to the binary file
    
    """
    
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load the binary files
    
    Args:
        path (Path): Path to the binary file
        
    Returns:
        Any: The object stored in the file
    
    """
    
    data = joblib.load(path)
    logger.info(f"Binary file loaded from {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Get the size in KB
    
    Args:
        path (Path): Path of the file
        
    Returns:
        str: The size in KB
    
    """
    
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

@ensure_annotations
def check_schema(path_of_csv: Path, schema: dict , path_of_status_file: Path) -> bool:
    """
    Validates the schema of the csv
    
    Args:
        path_of_csv (Path): The path of the CSV
        path_of_status_file (Path): The path of the status file
        
    Returns:
        str: If the CSV is validated
    
    """
    
    data = pd.read_csv(path_of_csv)
    all_columns = list(data.columns)
    all_schema = schema.keys()
    
    validation_status = None
    
    with open(path_of_status_file, 'w') as f:
        f.write(f"Validation status: Not Started")

        for col in all_columns:
            if col not in all_schema:
                validation_status = False
                with open(path_of_status_file, 'w') as f:
                    f.write(f"Validation status:  {validation_status}")
            else:
                validation_status = True
                with open(path_of_status_file, 'w') as f:
                    f.write(f"Validation status: {validation_status}")
        return validation_status
    
    