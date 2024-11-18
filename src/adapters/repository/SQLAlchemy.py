from typing import List

import logging

from domain.device.repository import DeviceRepository
from domain.device.model import Device

from adapters.database.SQLAlchemy import Device as SQLAlchemyDevice, SessionLocal

logger = logging.getLogger(__name__)

class SQLAlchemyDeviceRepository(DeviceRepository):
    def add(self, description) -> Device:
        logger.info(f"Adding device with description: {description}")
        with SessionLocal() as db:
            new_device = SQLAlchemyDevice(description=description)
            db.add(new_device)
            db.commit()
            
            if new_device is None:
                raise ValueError(f"Device with description {description} not found, device creation failed")

            logger.info(f"Device with description {new_device.description} added, ID: {new_device.id}")

            return Device(new_device.id, new_device.description) # type: ignore

    def get(self, device_id) -> Device | None:
        logger.info(f"Getting device with ID: {device_id}")
        with SessionLocal() as db:
            orm_device = db.query(SQLAlchemyDevice).filter(SQLAlchemyDevice.id == device_id).first()

        if orm_device is None:
            return None

        return Device(orm_device.id, orm_device.description) # type: ignore

    def get_all(self) -> List[Device]:
        logger.info("Getting all devices")
        with SessionLocal() as db:
            orm_devices = db.query(SQLAlchemyDevice).all()

        return [Device(orm_device.id, orm_device.description) for orm_device in orm_devices] # type: ignore

    def delete(self, device_id) -> Device:
        logger.info(f"Deleting device with ID: {device_id}")
        with SessionLocal() as db:
            orm_device = db.query(SQLAlchemyDevice).filter(SQLAlchemyDevice.id == device_id).first()

            if orm_device is None:
                raise ValueError(f"Device with ID {device_id} not found")

            db.delete(orm_device)
            db.commit()

            logger.info(f"Device with ID {device_id} deleted")

        return Device(orm_device.id, orm_device.description) # type: ignore
