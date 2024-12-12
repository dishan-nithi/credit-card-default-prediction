from src.default_predictor import logger
from default_predictor.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from default_predictor.pipeline.stage_02_data_validation import DataValidationTrainingPipeline

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

