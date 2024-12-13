# credit-card-default-prediction
credit card default prediction model

import dagshub
dagshub.init(repo_owner='dishan-nithi', repo_name='credit-card-default-prediction', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)

  export MLFLOW_TRACKING_URI=https://dagshub.com/dishan-nithi/credit-card-default-prediction.mlflow
  export MLFLOW_TRACKING_USERNAME=dishan-nithi
  export MLFLOW_TRACKING_PASSWORD=f9555631638b9db78b3221c99340c604de4fe75d