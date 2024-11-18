import logging

from domain.device.repository import DeviceRepository

logger = logging.getLogger(__name__)

class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        logger.info("Creating DeviceService")
        self.device_repository = device_repository

    def get_device(self, device_id):
        logger.info(f"Getting device with ID: {device_id}")
        return self.device_repository.get(device_id)

    def get_devices(self):
        logger.info("Getting all devices")
        return self.device_repository.get_all()

    def add_device(self, description: str):
        logger.info(f"Adding device with description: {description}")
        return self.device_repository.add(description)

    def delete_device(self, device_id):
        logger.info(f"Deleting device with ID: {device_id}")
        return self.device_repository.delete(device_id)
