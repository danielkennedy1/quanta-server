from domain.device.repository import DeviceRepository

class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def get_device(self, device_id):
        return self.device_repository.get(device_id)

    def get_devices(self):
        return self.device_repository.get_all()

    def add_device(self, description: str):
        return self.device_repository.add(description)

    def delete_device(self, device_id):
        return self.device_repository.delete(device_id)
