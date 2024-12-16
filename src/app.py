from connexion import App
from connexion.resolver import RelativeResolver
import logging

from config.config import config
from adapters.database.SQLAlchemy import engine, init_db
from adapters.dash.dash import init_dashboard
from adapters.controller.controller import * # instantiate controllers

from adapters.controller.interface_controller import index

logger = logging.getLogger(__name__)

config.logging.configure_logger(logging.getLogger())
config.logging.configure_logger(logging.getLogger('uvicorn'))
config.logging.configure_logger(logging.getLogger('uvicorn.access'))
config.logging.configure_logger(logging.getLogger('uvicorn.warning'))

logging.getLogger().setLevel(logging._nameToLevel[config.logging.log_level])

app = App(__name__)

logger.info(f"Loading API from {config.api.spec_file}")
app.add_api(config.api.spec_file, resolver=RelativeResolver(config.api.resolver))

app.add_url_rule("/", "index", index)

init_db(engine, delete_existing=False)

init_dashboard(app.app)


if __name__ == "__main__":
    app.run(port=config.api.port)
