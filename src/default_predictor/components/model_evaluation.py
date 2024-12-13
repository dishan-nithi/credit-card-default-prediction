import os
import pandas as pd
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
from urllib.parse import urlparse
import mlflow
from mlflow import sklearn, xgboost
import joblib
from default_predictor.entity.config_entity import ModelEvaluationConfig
from default_predictor.utils.common import save_json
from pathlib import Path


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        
    def eval_metrics(self, actual, pred):
        roc_auc = roc_auc_score(actual, pred)
        f1 = f1_score(actual, pred)
        precision = precision_score(actual, pred)
        recall = recall_score(actual, pred)
        accuracy = accuracy_score(actual, pred)
        return roc_auc, f1, precision, recall, accuracy
    
    def log_into_mlflow(self):
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)
        
        X_test = test_data.drop([self.config.target_column], axis=1)
        y_test = test_data[[self.config.target_column]]
        
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
        with mlflow.start_run():
            y_pred = model.predict(X_test)
            (roc_auc, f1, precision, recall, accuracy) = self.eval_metrics(y_test, y_pred)
            scores ={"roc_auc":roc_auc, "f1":f1, "precision":precision, "recall":recall, "accuracy":accuracy}
            save_json(path=Path(self.config.metric_file_name),data=scores)
            
            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("roc_auc", roc_auc)
            mlflow.log_metric("f1", f1)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("accuracy", accuracy)
            
            if tracking_url_type_store != "file":
                mlflow.xgboost.log_model(model, "model", registered_model_name="XGBoostModel")

            else:
                mlflow.xgboost.log_model(model, "model")


                