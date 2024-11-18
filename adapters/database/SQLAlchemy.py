from sqlalchemy import Column, Engine, Integer, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
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
    data_type = Column(Text)

    messages = relationship("Message", back_populates="metric")

    def __repr__(self):
        return f"Metric(id={self.id!r}, name={self.name!r}, data_type={self.data_type!r})"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    metric_id = Column(Integer, ForeignKey("metrics.id"))
    value = Column(Text)

    device = relationship("Device", back_populates="messages")
    metric = relationship("Metric", back_populates="messages")

    def __repr__(self):
        return f"Message(id={self.id!r}, device_id={self.device_id!r}, metric_id={self.metric_id!r}, value={self.value!r})"

def init_db(engine: Engine, delete_existing: bool = False):
    if delete_existing:
        logger.info("Deleting existing database")
        Base.metadata.drop_all(bind=engine)
    logger.info("Initializing database")
    Base.metadata.create_all(bind=engine)
