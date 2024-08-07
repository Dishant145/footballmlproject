

import os
import sys
from src.footballproject.exception import CustomException
from src.footballproject.logger import logging
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    # train_data_path:str=os.path.join('artifact','train.csv')
    # test_data_path:str=os.path.join('artifact','test.csv')
    raw_data_path:str=os.path.join('artifact','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            data = pd.read_csv('../data/mergedleagues.csv')
            
            logging.info("Reading raw dataset")
            
            # os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
        
            logging.info("Initiating Train Test Split")

            # train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            # train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            # test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of data is completed")

            return self.ingestion_config.raw_data_path
                # self.ingestion_config.train_data_path,
                # self.ingestion_config.test_data_path
                

        except Exception as e:
            raise CustomException(e,sys)


if __name__ == '__main__':
    logging.info("The data ingestion component execution has started")
    
    data_ingestion=DataIngestion()
    raw_data_path=data_ingestion.initiate_data_ingestion()