from connexion import App
from connexion.resolver import RelativeResolver
import logging

from config.config import config
from adapters.database.SQLAlchemy import engine, init_db, SessionLocal, Device

app = App(__name__)
app.add_api(config.api.spec_file, resolver=RelativeResolver(config.api.resolver))

config.logging.configure_logger(logging.getLogger())
config.logging.configure_logger(logging.getLogger('uvicorn'))
config.logging.configure_logger(logging.getLogger('uvicorn.access'))
config.logging.configure_logger(logging.getLogger('uvicorn.warning'))

init_db(engine)

with SessionLocal() as session:
    session.add(Device(description="Device 1"))
