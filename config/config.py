import json
import logging
import coloredlogs
import sys

class Config:
    def __init__(self, config_file_path: str):
        with open(config_file_path) as config_file:
            self.config = json.load(config_file)
        self.log_file = self.config['log']['file']
        self.log_level = self.config['log']['level']

    def get(self, key):
        return self.config[key]

    def configure_logger(self, logger: logging.Logger):
        logger.handlers = []
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging._nameToLevel[self.log_level])
        logger.addHandler(file_handler)
        
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging._nameToLevel[self.log_level])
        logger.addHandler(stdout_handler)
        
        coloredlogs.install(level=self.log_level, logger=logger)
