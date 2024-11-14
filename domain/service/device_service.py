from repository.device_repository import DeviceRepository

class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def get_device(self, device_id):
        return self.device_repository.get(device_id)

    def get_devices(self):
        return self.device_repository.get_all()

    def add_device(self, device):
        return self.device_repository.add(device)

    def delete_device(self, device_id):
        return self.device_repository.delete(device_id)
