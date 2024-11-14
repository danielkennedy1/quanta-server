from abc import ABC, abstractmethod

class DeviceController(ABC):
    @abstractmethod
    def getAll(self) -> list:
        """Retrieve a list of all devices."""
        pass
    
    @abstractmethod
    def create(self, device) -> dict:
        """Register a new device."""
        pass
    
    @abstractmethod
    def getById(self, id) -> dict | None:
        """Retrieve a specific device by ID."""
        pass
    
    @abstractmethod
    def deleteById(self, id) -> dict:
        """Delete a specific device by ID."""
        pass

class MockDeviceController(DeviceController):
    def getAll(self):
        return [
            {"id": 1, "description": "Temperature Sensor in Room 101"},
            {"id": 2, "description": "Pressure Sensor in Room 202"}
        ]
    
    def create(self, device):
        return {"id": device.get("id", 3), "description": device.get("description", "Humidity Sensor in Room 103")}
    
    def getById(self, id):
        if id == 1:
            return {"id": 1, "description": "Temperature Sensor in Room 101"}
        return None  # "not found" case
    
    def deleteById(self, id):
        return None  # Returns None to signify successful deletion
