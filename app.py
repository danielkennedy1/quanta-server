from connexion import App
from connexion.resolver import RelativeResolver
from config.config import Config
import logging

config = Config("config/config.json")
config.configure_logger(logging.getLogger())

app = App(__name__)
app.add_api('api.yaml', resolver=RelativeResolver("adapters.controller.controller"))
