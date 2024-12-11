from src.default_predictor import logger
from default_predictor.pipeline.stage_01_data_ingestion import DataIngestionPipeline

STAGE_NAME = 'DATA INGESTION'

if __name__ == '__main__':
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<\n\n")
    except Exception as e:
        logger.exception(e)
        raise e