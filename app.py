from connexion import App
from connexion.resolver import RelativeResolver
from config.config import Config
import logging

logger = logging.getLogger(__name__)

config = Config("config/config.json")
config.configure_logger(logger)

app = App(__name__)

app.add_api('api.yaml', resolver=RelativeResolver("adapters.controller.controller"))

#config.configure_logger(logging.getLogger("uvicorn.access"))
#config.configure_logger(logging.getLogger("uvicorn.error"))

logger.error("\n".join(logging.root.manager.loggerDict.keys()))
