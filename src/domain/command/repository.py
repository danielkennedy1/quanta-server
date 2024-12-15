from abc import ABC, abstractmethod
from typing import List

from domain.command.model import Command

class CommandRepository(ABC):
    @abstractmethod
    def add(self, device_id: int, command: str) -> Command:
        pass

    @abstractmethod
    def read_by_device_id(self, device_id: int) -> List[str]:
        pass
