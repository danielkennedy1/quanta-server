from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from domain.message.model import Message

class MessageRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Message]:
        pass

    @abstractmethod
    def get(self, message_id: int) -> Message | None:
        pass

    @abstractmethod
    def create(self, device_id: int, metric_id: int, value: str, datetime: datetime) -> Message:
        pass

    @abstractmethod
    def delete(self, message_id: int) -> Message:
        pass
