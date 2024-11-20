from datetime import datetime
from typing import List

from domain.device.repository import DeviceRepository
from domain.metric.repository import MetricRepository

from domain.message.model import Message
from domain.message.repository import MessageRepository


class MessageService:
    def __init__(self, 
                 message_repository: MessageRepository,
                 device_repository: DeviceRepository,
                 metric_repository: MetricRepository
                 ):
        self.message_repository = message_repository
        self.device_repository = device_repository
        self.metric_repository = metric_repository

    def get_all(self, device_id = None, metric_id = None) -> List[Message]:
        if device_id is None and metric_id is None:
            return self.message_repository.get_all()

        if device_id is not None and metric_id is not None:
            return self.message_repository.get_all_by_device_and_metric(device_id, metric_id)

        raise ValueError("Neither or both of device_id and metric_id must be provided")

    def get(self, message_id: int) -> Message:

        message = self.message_repository.get(message_id)
        if message is None:
            raise ValueError(f"Message with ID {message_id} not found")

        return message

    def create(self, device_id: int, metric_id: int, metric_value: str, datetime: datetime) -> Message:
        if self.device_repository.get(device_id) is None:
            raise ValueError(f"Device with ID {device_id} does not exist")
        if self.metric_repository.get(metric_id) is None:
            raise ValueError(f"Metric with ID {metric_id} does not exist")

        return self.message_repository.create(device_id, metric_id, metric_value, datetime)

    def delete(self, message_id: int) -> Message:
        return self.message_repository.delete(message_id)
