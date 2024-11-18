from abc import ABC, abstractmethod
import logging
from flask import Response

from quanta_client.models.metric import Metric as ApiMetric

from domain.metric.service import MetricService

from adapters.controller.util import convert_to_api

logger = logging.getLogger(__name__)

class MetricController(ABC):
    @abstractmethod
    def getAll(self) -> Response:
        """Retrieve a list of all metrics."""
        pass
    
    @abstractmethod
    def create(self, body) -> Response:
        """Register a new metric."""
        pass
    
    @abstractmethod
    def getById(self, id) -> Response:
        """Retrieve a specific metric by ID."""
        pass
    
    @abstractmethod
    def deleteById(self, id) -> Response:
        """Delete a specific metric by ID."""
        pass

class MockMetricController(MetricController):
    def getAll(self):
        return Response(str([
            {"id": 1, "name": "Temperature", "data_type": "float"},
            {"id": 2, "name": "Humidity", "data_type": "integer"}
        ]), status=200)
    
    def create(self, body):
        return Response(str({"id": body.get("id", 3), "name": body.get("name", "Pressure"), "data_type": body.get("data_type", "float")}), status=201)
    
    def getById(self, id):
        return Response(str({"id": 1, "name": "Temperature", "data_type": "float"}), status=200) if id == 1 else Response("Metric not found", status=404)
    
    def deleteById(self, id):
        return Response(str({"id": id, "name": "Temperature", "data_type": "float"}), status=200) if id == 1 else Response("Metric not found", status=404)

class RestMetricController(MetricController):
    def __init__(self, metricService: MetricService):
        logger.info("Creating RestMetricController")
        self.metricService = metricService

    def getAll(self) -> Response:
        all_metrics = [convert_to_api(metric).to_json() for metric in self.metricService.get_all()] # type: ignore
        if len(all_metrics) > 0:
            # FIXME: Responses with lists arent right
            return Response(str(all_metrics), status=200)
        return Response("No metrics found", status=404) # type: ignore
    
    def create(self, body) -> Response:
        logger.info(f"Creating metric with body: {body}")
        metric = ApiMetric.from_dict(body)
        if metric is None:
            return Response("Invalid JSON", status=400)
        created_metric = self.metricService.add(metric.name, metric.data_type)
        if created_metric is None:
            return Response("Failed to create metric", status=500)
        return Response(convert_to_api(created_metric).to_json(), status=201) # type: ignore
    
    def getById(self, id) -> Response:
        metric = self.metricService.get(id)
        if metric is None:
            return Response("Metric not found", status=404)
        return Response(convert_to_api(metric).to_json(), status=200) # type: ignore
    
    def deleteById(self, id) -> Response:
        metric = self.metricService.delete(id)
        if metric is None:
            return Response("Metric not found", status=404)
        return Response(convert_to_api(metric).to_json(), status=200) # type: ignore

