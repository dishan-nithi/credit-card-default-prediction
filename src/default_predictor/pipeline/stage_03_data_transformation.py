from default_predictor.config.configuration import ConfigurationManager
from default_predictor.components.data_transformation import DataTransformation
from default_predictor import logger
from pathlib import Path

STAGE_NAME = "DATA TRANSFORMATION"

class DataTransformationPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"),"r") as f:
                status = f.read().split(" ")[-1]
            
            if status == 'True':
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_splitting()
            else:
                raise Exception("Invalid data schema.")

        except Exception as e:
            print(e)
            
            
if __name__ == '__main__':
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        obj = DataTransformationPipeline()
        obj.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e