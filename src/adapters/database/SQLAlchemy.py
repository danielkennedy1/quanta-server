from sqlalchemy import Column, DateTime, Engine, Integer, Text, ForeignKey, create_engine
from sqlalchemy.orm import mapped_column, relationship, declarative_base, sessionmaker
from config.config import config
import logging

logger = logging.getLogger(__name__)

engine = create_engine(config.database.connection_string, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)

    messages = relationship("Message", back_populates="device")

    def __repr__(self):
        return f"Device(id={self.id!r}, description={self.description!r})"

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    type_name = Column(Text)

    messages = relationship("Message", back_populates="metric")

    def __repr__(self):
        return f"Metric(id={self.id!r}, name={self.name!r}, data_type={self.data_type!r})"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)

    device_id = mapped_column(ForeignKey("devices.id"))
    device = relationship("Device", lazy="joined")

    metric_id = mapped_column(ForeignKey("metrics.id"))
    metric = relationship("Metric", lazy="joined")

    value = Column(Text)
    datetime = Column(DateTime)

    def __repr__(self):
        return f"Message(id={self.id!r}, device_id={self.device_id!r}, metric_id={self.metric_id!r}, value={self.value!r})"

def init_db(engine: Engine, delete_existing: bool = False):
    logger.info("Initializing database")
    if delete_existing:
        logger.warning("Deleting existing database")
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
