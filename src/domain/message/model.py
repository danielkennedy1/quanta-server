from dataclasses import dataclass

from domain.device.model import Device
from domain.metric.model import Metric

@dataclass
class Message:
    id: int
    device: Device
    metric: Metric
    value: str
