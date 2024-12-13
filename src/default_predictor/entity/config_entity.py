from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    token: str
 
@dataclass(frozen=True)   
class DataValidationConfig:
    root_dir: Path
    status_file: str
    unzip_data_dir: Path
    all_schema: dict
    
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    
@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    scale_pos_weight: int
    max_depth: int
    min_child_weight: int
    subsample: float
    colsample_bytree: float
    objective: str
    eta: float
    gamma: float
    n_estimators: int 
    enable_categorical: str
    eval_metric: str
    alpha: float
    target_column: str
    
@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str