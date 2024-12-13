from src.default_predictor import logger
from default_predictor.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from default_predictor.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from default_predictor.pipeline.stage_03_data_transformation import DataTransformationPipeline
from default_predictor.pipeline.stage_04_model_trainer import ModelTrainerPipeline

STAGE_NAME = 'DATA INGESTION'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<")
except Exception as e:
    logger.exception(e)
    raise e
    
STAGE_NAME = 'DATA VALIDATION'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = 'DATA TRANSFORMATION'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_transformation = DataTransformationPipeline()
    data_transformation.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<")
except Exception as e:
    raise e

STAGE_NAME = 'MODEL TRAINER'

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    model_trainer = ModelTrainerPipeline()
    model_trainer.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<")
except Exception as e:
    raise e