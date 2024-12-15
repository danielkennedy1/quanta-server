from abc import ABC, abstractmethod
from flask import Response
import logging

from quanta_client.models.command import Command as ApiCommand

from domain.command.service import CommandService

from adapters.controller.util import convert_command_to_api

logger = logging.getLogger(__name__)

class CommandController(ABC):
    @abstractmethod
    def send(self, body) -> Response:
        """Send a command to a device."""
        pass

    @abstractmethod
    def getByDeviceId(self, deviceId) -> Response:
        """Retrieve a list of all commands for a specific device."""
        pass


class RestCommandController(CommandController):
    def __init__(self, command_service: CommandService):
        logger.info("Creating RestCommandController")
        self.command_service = command_service

    def send(self, body) -> Response:
        device_id = body.get("device_id")
        command = body.get("command")
        logger.info(f"Sending command to device with ID {device_id}")

        created_command =  self.command_service.send(device_id, command)

        logger.info(f"Command {command} sent to device with ID {device_id}")

        return Response(status=201, response=convert_command_to_api(created_command).to_json()) # type: ignore
    

    def getByDeviceId(self, deviceId) -> Response:
        logger.info(f"Getting all commands for device with ID {deviceId}")
        commands = self.command_service.get_by_device_id(deviceId)

        if len(commands) == 0:
            logger.warning(f"No commands found for device with ID {deviceId}")
            return Response(status=404, response="No commands found for device with ID {device_id}")

        logger.info(f"Found {len(commands)} commands for device with ID {deviceId}")

        return Response(status=200, response=[convert_command_to_api(command).to_json() for command in commands]) # type: ignore
