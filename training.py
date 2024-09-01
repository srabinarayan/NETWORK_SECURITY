import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from networksecurity.pipelines.training_pipeline import TrainingPipeline

def start_training():
    try:
        logging.info("training has started")
        pipeline = TrainingPipeline()
        pipeline.run()
    except Exception as e:
        raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    start_training()    