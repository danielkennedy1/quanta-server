from dataclasses import dataclass

@dataclass
class Metric:
    id: int
    name: str
    data_type: str