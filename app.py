from connexion import App
from connexion.resolver import RelativeResolver
from config.config import Config
import logging

logger = logging.getLogger(__name__)

config = Config("config/config.json")
config.configure_logger(logger)

uvicorn_logger = logging.getLogger("uvicorn")
config.configure_logger(uvicorn_logger)

app = App(__name__)

app.add_api('api.yaml', resolver=RelativeResolver("adapters.controller.controller"))
