from abc import ABC, abstractmethod

# TODO: Response validation

class MetricController(ABC):
    @abstractmethod
    def getAll(self) -> list:
        """Retrieve a list of all metrics."""
        pass
    
    @abstractmethod
    def create(self, metric) -> dict:
        """Register a new metric."""
        pass
    
    @abstractmethod
    def getById(self, id) -> dict | None:
        """Retrieve a specific metric by ID."""
        pass
    
    @abstractmethod
    def deleteById(self, id) -> dict:
        """Delete a specific metric by ID."""
        pass

class MockMetricController(MetricController):
    def getAll(self):
        return [
            {"id": 1, "name": "Temperature", "data_type": "float"},
            {"id": 2, "name": "Humidity", "data_type": "integer"}
        ]
    
    def create(self, metric):
        return {
            "id": metric.get("id", 3),
            "name": metric.get("name", "Pressure"),
            "data_type": metric.get("data_type", "float")
        }
    
    def getById(self, id):
        if id == 1:
            return {"id": 1, "name": "Temperature", "data_type": "float"}
        return None  # Simulates a "not found" case
    
    def deleteById(self, id):
        return None  # Returns None to signify successful deletion
