from connexion import App
from connexion.resolver import RelativeResolver
import logging

from config.config import config
from adapters.database.SQLAlchemy import engine, init_db
from adapters.dash.dash import init_dashboard

logger = logging.getLogger(__name__)

config.logging.configure_logger(logging.getLogger())
config.logging.configure_logger(logging.getLogger('uvicorn'))
config.logging.configure_logger(logging.getLogger('uvicorn.access'))
config.logging.configure_logger(logging.getLogger('uvicorn.warning'))

app = App(__name__)

logger.info(f"Loading API from {config.api.spec_file}")
app.add_api(config.api.spec_file, resolver=RelativeResolver(config.api.resolver))

init_db(engine, delete_existing=False)

init_dashboard(app.app)


if __name__ == "__main__":
    app.run(port=config.api.port)
