from default_predictor.config.configuration import ConfigurationManager
from default_predictor.components.model_evaluation import ModelEvaluation
from default_predictor import logger
from pathlib import Path

STAGE_NAME = 'MODEL EVALUATION'

class ModelEvaluationPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation_config = ModelEvaluation(config=model_evaluation_config)
        model_evaluation_config.log_into_mlflow()
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        obj = ModelEvaluationPipeline()
        obj.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<")
    except Exception as e:
        raise e
    