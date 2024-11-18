from typing import List

from domain.device.repository import DeviceRepository
from domain.device.model import Device

from adapters.database.SQLAlchemy import Device as SQLAlchemyDevice, SessionLocal

class SQLAlchemyDeviceRepository(DeviceRepository):
    def add(self, description) -> Device:
        with SessionLocal() as db:
            db.add(SQLAlchemyDevice(description=description))
            db.commit()
            device = db.query(SQLAlchemyDevice).filter(SQLAlchemyDevice.description == description).first()
            
            if device is None:
                raise ValueError(f"Device with description {description} not found, device creation failed")

            return Device(device[0].id, device[0].description)

    def get(self, device_id) -> Device | None:
        with SessionLocal() as db:
            orm_device = db.query(SQLAlchemyDevice).filter(SQLAlchemyDevice.id == device_id).first()

        if orm_device is None:
            return None

        return Device(orm_device[0].id, orm_device[0].description)

    def get_all(self) -> List[Device]:
        with SessionLocal() as db:
            orm_devices = db.query(SQLAlchemyDevice).all()

        orm_devices = [orm_device[0] for orm_device in orm_devices]

        return [Device(orm_device.id, orm_device.description) for orm_device in orm_devices]

    def delete(self, device_id) -> Device:
        with SessionLocal() as db:
            orm_device = db.query(SQLAlchemyDevice).filter(SQLAlchemyDevice.id == device_id).first()

            if orm_device is None:
                raise ValueError(f"Device with ID {device_id} not found")

            db.delete(orm_device)
            db.commit()

        return Device(orm_device[0].id, orm_device[0].description)
