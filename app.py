import os
import sys
from src.footballproject.logger import logging
from src.footballproject.exception import CustomException
from src.footballproject.components.data_ingestion import DataIngestion


if __name__ == "__main__":
    logging.info("The execution has started")

    try:
        data_ingestion_obj=DataIngestion()
        data_ingestion_obj.initiate_data_ingestion()

    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e,sys)
