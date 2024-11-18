import json
import logging
import sys
import coloredlogs

logger = logging.getLogger(__name__)


class Config:
    _instance = None

    def __new__(cls, config_file_path: str):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize(config_file_path)
        return cls._instance

    def _initialize(self, config_file_path: str):
        with open(config_file_path) as config_file:
            self.config = json.load(config_file)

        if not self.config:
            raise ValueError("Config file is empty")

        if not self.config.get('log'):
            logger.warning("No logging configuration found in config file")
        if not self.config.get('database'):
            logger.warning("No database configuration found in config file")
        if not self.config.get('api'):
            logger.warning("No API configuration found in config file")
        
        self.logging = self.LoggingConfig(self.config.get('log', {}))
        self.database = self.DatabaseConfig(self.config.get('database', {}))
        self.api = self.ApiConfig(self.config.get('api', {}))

    def get(self, key):
        """Access configuration settings by key."""
        return self.config.get(key)

    class LoggingConfig:
        def __init__(self, log_config):
            self.log_file = log_config.get('file', 'default.log')
            self.log_level = log_config.get('level', 'INFO')

        def configure_logger(self, logger: logging.Logger):
            logger.handlers = []

            # File handler
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging._nameToLevel[self.log_level.upper()])
            logger.addHandler(file_handler)

            # Standard output handler
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging._nameToLevel[self.log_level.upper()])
            logger.addHandler(stdout_handler)

            coloredlogs.install(level=self.log_level.upper(), logger=logger)

    class DatabaseConfig:
        def __init__(self, db_config):
            self.connection_string = db_config.get('connection_string', 'sqlite:///:memory:')

    class ApiConfig:
        def __init__(self, api_config):
            self.spec_file = api_config.get('spec_file', 'swagger.yaml')
            self.resolver = api_config.get('resolver', '')
            self.port = api_config.get('port', 8080)
            self.server = api_config.get('server', 'localhost')

config = Config("config/config.json")
