from dataclasses import dataclass

@dataclass
class Device:
    id: int
    description: str

@dataclass
class Metric:
    id: int
    name: str
    data_type: str

@dataclass
class Message:
    id: int
    device_id: int
    metric_id: int
    value: str
