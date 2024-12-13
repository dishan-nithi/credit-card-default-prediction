import pandas as pd
import os
from default_predictor import logger
from xgboost import XGBClassifier
import joblib
from default_predictor.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        
    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        
        X_train = train_data.drop([self.config.target_column],axis=1)
        X_test = test_data.drop([self.config.target_column],axis=1)
        y_train = train_data[[self.config.target_column]]
        y_test = test_data[[self.config.target_column]]
        
        params = {
        "scale_pos_weight" : self.config.scale_pos_weight,
        "max_depth" : self.config.max_depth,
        "min_child_weight" : self.config.min_child_weight,
        "subsample" : self.config.subsample,
        "colsample_bytree" : self.config.colsample_bytree,
        "objective" : self.config.objective,
        "eta" : self.config.eta,
        "gamma" : self.config.gamma,
        "n_estimators" : self.config.n_estimators ,
        "enable_categorical" : self.config.enable_categorical,
        "eval_metric" : self.config.eval_metric,
        "alpha" : self.config.alpha
        }
        
        clf = XGBClassifier(**params, random_state=42)
        clf.fit(X_train, y_train)
        
        joblib.dump(clf, os.path.join(self.config.root_dir, self.config.model_name))