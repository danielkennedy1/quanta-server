from typing import List
import logging

from domain.metric.model import Metric
from domain.metric.repository import MetricRepository

logger = logging.getLogger(__name__)

class MetricService(object):
    def __init__(self, metric_repository: MetricRepository):
        logger.info("Creating MetricService")
        self.metric_repository = metric_repository

    def add(self, name: str, type_name: str) -> Metric:
        logger.info(f"Adding metric with name: {name} and type: {type_name}")
        return self.metric_repository.add(name, type_name)
        
    def get(self, metric_id) -> Metric | None:
        logger.info(f"Getting metric with ID: {metric_id}")
        return self.metric_repository.get(metric_id)

    def get_all(self) -> List[Metric]:
        logger.info("Getting all metrics")
        return self.metric_repository.get_all()

    def delete(self, metric_id) -> Metric:
        logger.info(f"Deleting metric with ID: {metric_id}")
        return self.metric_repository.delete(metric_id)
