from typing import List

import logging

from sqlalchemy.orm import joinedload

from domain.message.repository import MessageRepository
from domain.message.model import Message

from adapters.database.SQLAlchemy import Message as SQLAlchemyMessage, Metric as SQLAlchemyMetric, Device as SQLAlchemyDevice, SessionLocal

logger = logging.getLogger(__name__)

class SQLAlchemyMessageRepository(MessageRepository):
    def get_all(self) -> List[Message]:
        logger.info("Getting all messages")
        with SessionLocal() as db:
            orm_messages = db.query(SQLAlchemyMessage).options(joinedload(SQLAlchemyMessage.device), joinedload(SQLAlchemyMessage.metric)).all()

        return [Message(orm_message.id, orm_message.device, orm_message.metric, orm_message.value, orm_message.datetime) for orm_message in orm_messages] # type: ignore

    def get_all_by_device_and_metric(self, device_id, metric_id) -> List[Message]:
        logger.info(f"Getting all messages with device ID: {device_id} and metric ID: {metric_id}")
        with SessionLocal() as db:
            orm_messages = db.query(SQLAlchemyMessage).options(joinedload(SQLAlchemyMessage.device), joinedload(SQLAlchemyMessage.metric)).filter(SQLAlchemyMessage.device_id == device_id, SQLAlchemyMessage.metric_id == metric_id).all()

        return [Message(orm_message.id, orm_message.device, orm_message.metric, orm_message.value, orm_message.datetime) for orm_message in orm_messages] # type: ignore

    def get(self, message_id) -> Message | None:
        logger.info(f"Getting message with ID: {message_id}")
        with SessionLocal() as db:
            orm_message = db.query(SQLAlchemyMessage).options(joinedload(SQLAlchemyMessage.device), joinedload(SQLAlchemyMessage.metric)).filter(SQLAlchemyMessage.id == message_id).first()

        if orm_message is None:
            return None

        logger.info(f"Message with ID {orm_message.id} found")
        logger.debug(f"orm_message: {orm_message}")

        return Message(orm_message.id, orm_message.device, orm_message.metric, orm_message.value, orm_message.datetime) # type: ignore

    def create(self, device_id, metric_id, value, datetime) -> Message:
        logger.info(f"Creating message with device ID: {device_id}, metric ID: {metric_id}, value: {value}, datetime: {datetime}")
        with SessionLocal() as db:
            new_message = SQLAlchemyMessage(device_id=device_id, metric_id=metric_id, value=value, datetime=datetime)
            db.add(new_message)
            db.commit()
            
            if new_message is None:
                raise ValueError(f"Message with device ID {device_id}, metric ID {metric_id}, value {value}, datetime {datetime} not found, message creation failed")

            logger.info(f"Message with device ID {new_message.device_id}, metric ID {new_message.metric_id}, value {new_message.value}, datetime {new_message.datetime} added, ID: {new_message.id}")

            logger.debug(f"new_message: {new_message}")

            return Message(new_message.id, new_message.device, new_message.metric, new_message.value, new_message.datetime) # type: ignore

    def delete(self, message_id) -> Message:
        logger.info(f"Deleting message with ID: {message_id}")
        with SessionLocal() as db:
            orm_message = db.query(SQLAlchemyMessage).options(joinedload(SQLAlchemyMessage.device), joinedload(SQLAlchemyMessage.metric)).filter(SQLAlchemyMessage.id == message_id).first()

            if orm_message is None:
                raise ValueError(f"Message with ID {message_id} not found")

            db.delete(orm_message)
            db.commit()

            logger.info(f"Message with ID {message_id} deleted")

        return Message(orm_message.id, orm_message.device_id, orm_message.metric_id, orm_message.value, orm_message.datetime) # type: ignore
