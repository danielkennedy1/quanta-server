from abc import ABC, abstractmethod
from domain.device.service import DeviceService
from domain.device.model import Device

import logging

logger = logging.getLogger(__name__)

class DeviceController(ABC):
    @abstractmethod
    def getAll(self) -> list:
        """Retrieve a list of all devices."""
        pass
    
    @abstractmethod
    def create(self, body) -> dict:
        """Register a new device."""
        pass
    
    @abstractmethod
    def getById(self, id) -> dict | None:
        """Retrieve a specific device by ID."""
        pass
    
    @abstractmethod
    def deleteById(self, body) -> dict:
        """Delete a specific device by ID."""
        pass

class MockDeviceController(DeviceController):
    def getAll(self):
        return [
            {"id": 1, "description": "Temperature Sensor in Room 101"},
            {"id": 2, "description": "Pressure Sensor in Room 202"}
        ]
    
    def create(self, body):
        return {"id": body.get("id", 3), "description": body.get("description", "Humidity Sensor in Room 103")}
    
    def getById(self, id):
        if id == 1:
            return {"id": 1, "description": "Temperature Sensor in Room 101"}
        return None  # "not found" case
    
    def deleteById(self, id):
        return None  # Returns None to signify successful deletion

class RestDeviceController(DeviceController):
    def __init__(self, deviceService: DeviceService):
        logger.info("Creating RestDeviceController")
        self.deviceService = deviceService

    def getAll(self):
        return self.deviceService.get_devices()
    
    def create(self, body):
        device = self.deviceService.add_device(body["description"])

        return {"id": device.id, "description": device.description}
    
    def getById(self, id):
        device = self.deviceService.get_device(id)
        if device is None:
            return None
        return {"id": device.id, "description": device.description}
    
    def deleteById(self, id):
        return self.deviceService.delete_device(id).__dict__
