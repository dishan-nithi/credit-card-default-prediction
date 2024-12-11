import os
import zipfile
from default_predictor import logger
import requests
from default_predictor.utils.common import get_size
from pathlib import Path
from default_predictor.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            '''filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )'''
            url = self.config.source_URL
            token = self.config.token
            headers = {
                'Authorization' : f'token {token}',
                'Accept' : 'application/vnd.github.v3.raw'
            }
            filename = url.split('/')[-1]
            filepath = self.config.root_dir
            
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                # Write the content to a local file
                with open(f'{filepath}/{filename}', 'wb') as file:
                    file.write(response.content)
                print("File downloaded successfully.")
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
            
            logger.info(f"{filename} downloaded.")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
            
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
                
                