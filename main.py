from src.default_predictor import logger
from default_predictor.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from default_predictor.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from default_predictor.pipeline.stage_03_data_transformation import DataTransformationPipeline
from default_predictor.pipeline.stage_04_model_trainer import ModelTrainerPipeline 
from default_predictor.pipeline.stage_05_data_evaluation import ModelEvaluationPipeline
import os, sys
from default_predictor import constants


os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/dishan-nithi/credit-card-default-prediction.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "dishan-nithi"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "f9555631638b9db78b3221c99340c604de4fe75d"

STAGE_NAME = 'DATA INGESTION'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<\n\n*****************")
except Exception as e:
    logger.exception(e)
    raise e
    
STAGE_NAME = 'DATA VALIDATION'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<\n\n*****************")
except Exception as e:
    logger.exception(e)
    raise e

with open(constants.STATUS_FILE_PATH,'r') as file:
    file_content = file.read()
    
if 'True' not in file_content:
    logger.info('The data is not valid. Please check the data source.')
    sys.exit(0)

STAGE_NAME = 'DATA TRANSFORMATION'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_transformation = DataTransformationPipeline()
    data_transformation.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<\n\n*****************")
except Exception as e:
    raise e

STAGE_NAME = 'MODEL TRAINER'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    model_trainer = ModelTrainerPipeline()
    model_trainer.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<\n\n*****************")
except Exception as e:
    raise e

STAGE_NAME = "MODEL EVALUATION"

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    model_evaluation = ModelEvaluationPipeline()
    model_evaluation.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<\n\n*****************")
except Exception as e:
    raise e