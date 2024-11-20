from datetime import datetime, timezone
from abc import ABC, abstractmethod
from flask import Response
import json

from quanta_client.models.message import Message as ApiMessage
from adapters.controller.util import convert_message_to_api
from domain.message.model import Message
from domain.message.service import MessageService

class MessageController(ABC):
    @abstractmethod
    def getAll(self, device_id, metric_id) -> Response:
        """Retrieve a list of all messages."""
        pass
    
    @abstractmethod
    def create(self, body) -> Response:
        """Record a new message."""
        pass
    
    @abstractmethod
    def getById(self, id) -> Response:
        """Retrieve a specific message by ID."""
        pass
    
    @abstractmethod
    def deleteById(self, id) -> Response:
        """Delete a specific message by ID."""
        pass


class MockMessageController(object):
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
    
    def create(self, body):
        return {
            "id": body.get("id", 3),
            "device_id": body.get("device_id", 3),
            "metric_id": body.get("metric_id", 3),
            "metric_value": body.get("metric_value", "1013.25"),
            "timestamp": body.get("timestamp", datetime.now(timezone.utc.utc).isoformat() + "Z")
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

class RestMessageController(MessageController):
    def __init__(self, message_service: MessageService):
        self.message_service = message_service
    
    def getAll(self, device_id = None, metric_id = None) -> Response:
        try:
            messages = self.message_service.get_all(device_id, metric_id)
        except ValueError as e:
            return Response(str(e), status=400)

        if len(messages) == 0:
            return Response("No messages found", status=404)

        messages = [convert_message_to_api(message).to_dict() for message in messages] # type: ignore

        return Response(json.dumps(messages), status=200)
    
    def create(self, body) -> Response:
        created_message = self.message_service.create(
            body.get("device_id"),
            body.get("metric_id"),
            body.get("metric_value"),
            datetime.strptime(body.get("timestamp"), "%Y-%m-%dT%H:%M:%SZ")
        )

        return Response(convert_message_to_api(created_message).to_json(), status=201) # type: ignore
    
    def getById(self, id) -> Response:
        try:
            message = self.message_service.get(id)
            return Response(ApiMessage.from_dict(message.__dict__).to_json(), status=200) # type: ignore
        except ValueError:
            return Response("Message not found", status=404)
    
    def deleteById(self, id) -> Response:
        try:
            deleted_message = self.message_service.delete(id)
            return Response(ApiMessage.from_dict(deleted_message.__dict__).to_json(), status=200) # type: ignore
        except ValueError:
            return Response("Message not found", status=404)
