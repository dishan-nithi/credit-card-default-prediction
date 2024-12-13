from default_predictor.config.configuration import ConfigurationManager
from default_predictor.components.model_trainer import ModelTrainer
from default_predictor import logger
from pathlib import Path


STAGE_NAME = 'MODEL TRAINER'

class ModelTrainerPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config)
        model_trainer_config.train()        

if __name__ == '__main__':
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        obj = ModelTrainerPipeline()
        obj.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<")
    except Exception as e:
        raise e