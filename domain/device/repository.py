from abc import ABC, abstractmethod
from domain.device.model import Device
from typing import List

class DeviceRepository(ABC):
    @abstractmethod
    def add(self, description) -> Device:
        pass

    @abstractmethod
    def get(self, device_id) -> Device | None:
        pass

    @abstractmethod
    def get_all(self) -> List[Device]:
        pass

    @abstractmethod
    def delete(self, device_id) -> Device:
        pass
