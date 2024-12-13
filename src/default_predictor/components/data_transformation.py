import os
from default_predictor import logger
from default_predictor.entity.config_entity import DataTransformationConfig
import pandas as pd
from sklearn.model_selection import train_test_split

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        
    def train_test_splitting(self):
        df = pd.read_csv(self.config.data_path)
        
        train, test = train_test_split(df, test_size=0.3)
        
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index = False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index = False)
        
        logger.info("Prepared training, testing datasets")
        logger.info(f"Training data shape {train.shape}")
        logger.info(f"Test data shape {test.shape}")
        