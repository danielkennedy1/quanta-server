from abc import ABC, abstractmethod
from flask import Response

from domain.device.service import DeviceService
from quanta_client.models.device import Device as ApiDevice

import logging

logger = logging.getLogger(__name__)

class DeviceController(ABC):
    @abstractmethod
    def getAll(self) -> Response:
        """Retrieve a list of all devices."""
        pass
    
    @abstractmethod
    def create(self, body) -> Response:
        """Register a new device."""
        pass
    
    @abstractmethod
    def getById(self, id) -> Response:
        """Retrieve a specific device by ID."""
        pass
    
    @abstractmethod
    def deleteById(self, id) -> Response:
        """Delete a specific device by ID."""
        pass

class MockDeviceController(DeviceController):
    def getAll(self):
        return Response(str([
            {"id": 1, "description": "Temperature Sensor in Room 101"},
            {"id": 2, "description": "Pressure Sensor in Room 202"}
        ]), status=200)
    
    def create(self, body):
        return Response(str({"id": body.get("id", 3), "description": body.get("description", "Humidity Sensor in Room 103")}), status=201)
    
    def getById(self, id):
        return Response(str({"id": 1, "description": "Temperature Sensor in Room 101"}), status=200) if id == 1 else Response("Device not found", status=404)
    
    def deleteById(self, id):
        return Response(str({"id": id, "description": "Temperature Sensor in Room 101"}), status=200) if id == 1 else Response("Device not found", status=404)

class RestDeviceController(DeviceController):
    def __init__(self, deviceService: DeviceService):
        logger.info("Creating RestDeviceController")
        self.deviceService = deviceService

    def getAll(self):
        # FIXME: Responses with lists arent right
        all_devices = [ApiDevice.from_dict(device.__dict__).to_json() for device in self.deviceService.get_devices()] # type: ignore
        if len(all_devices) > 0:
            return Response(str(all_devices), status=200)
        return Response("No devices found.", status=404)
    
    def create(self, body):
        device = ApiDevice.from_dict(body)
        if device is None: # Invalid JSON
            return Response("Invalid JSON", status=400)

        created_device = self.deviceService.add_device(str(device.description))

        response_device = ApiDevice.from_dict(created_device.__dict__)

        assert response_device is not None

        return Response(response_device.to_json(), status=201)
    
    def getById(self, id):
        device = self.deviceService.get_device(id)
        if device is None:
            return Response("Device not found", status=404)
        return Response(ApiDevice.from_dict(device.__dict__).to_json()) # type: ignore
    
    def deleteById(self, id):
        return Response(str(self.deviceService.delete_device(id).__dict__), status=200)
