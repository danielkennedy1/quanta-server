from datetime import datetime, timezone
from abc import ABC, abstractmethod

class MessageController(ABC):
    @abstractmethod
    def getAll(self) -> list:
        """Retrieve a list of all messages."""
        pass
    
    @abstractmethod
    def create(self, message) -> dict:
        """Record a new message."""
        pass
    
    @abstractmethod
    def getById(self, id) -> dict | None:
        """Retrieve a specific message by ID."""
        pass
    
    @abstractmethod
    def deleteById(self, id) -> dict:
        """Delete a specific message by ID."""
        pass


class MockMessageController(MessageController):
    def getAll(self):
        return [
            {
                "id": 1,
                "device_id": 1,
                "metric_id": 1,
                "metric_value": "23.5",
                "timestamp": "2023-10-01T12:30:00Z"
            },
            {
                "id": 2,
                "device_id": 2,
                "metric_id": 2,
                "metric_value": "55",
                "timestamp": "2023-10-01T12:35:00Z"
            }
        ]
    
    def create(self, message):
        return {
            "id": message.get("id", 3),
            "device_id": message.get("device_id", 3),
            "metric_id": message.get("metric_id", 3),
            "metric_value": message.get("metric_value", "1013.25"),
            "timestamp": message.get("timestamp", datetime.now(timezone.utc.utc).isoformat() + "Z")
        }
    
    def getById(self, id):
        if id == 1:
            return {
                "id": 1,
                "device_id": 1,
                "metric_id": 1,
                "metric_value": "23.5",
                "timestamp": "2023-10-01T12:30:00Z"
            }
        return None  # Simulates a "not found" case
    
    def deleteById(self, id):
        return None  # Returns None to signify successful deletion
