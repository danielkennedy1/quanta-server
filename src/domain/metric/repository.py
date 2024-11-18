from abc import ABC, abstractmethod
from typing import List

from domain.metric.model import Metric

class MetricRepository(ABC):
    @abstractmethod
    def add(self, name, type_name) -> Metric:
        pass

    @abstractmethod
    def get(self, metric_id) -> Metric | None:
        pass

    @abstractmethod
    def get_all(self) -> List[Metric]:
        pass

    @abstractmethod
    def delete(self, metric_id) -> Metric:
        pass
