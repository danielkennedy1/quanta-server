from dataclasses import dataclass

@dataclass
class Message:
    id: int
    device_id: int
    metric_id: int
    value: str
