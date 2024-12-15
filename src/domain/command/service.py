from typing import List
import logging

from domain.device.repository import DeviceRepository

from domain.command.repository import CommandRepository
from domain.command.model import Command

logger = logging.getLogger(__name__)

class CommandService:
    def __init__(self, device_repository: DeviceRepository, command_repository: CommandRepository):
        self.device_repository = device_repository
        self.command_repository = command_repository

    def send(self, device_id: int, command: str) -> Command:
        logger.info(f"Adding command {command} to device with ID {device_id}")
        if self.device_repository.get(device_id) is None:
            raise ValueError(f"Device with ID {device_id} does not exist")

        return self.command_repository.add(device_id, command)

    def get_by_device_id(self, device_id: int) -> List[Command]:
        logger.info(f"Getting all commands for device with ID {device_id}")
        device = self.device_repository.get(device_id)
        if device is None:
            raise ValueError(f"Device with ID {device_id} does not exist")

        command_strings = self.command_repository.read_by_device_id(device_id)

        commands = [Command(device, command_string) for command_string in command_strings]

        logger.info(f"Found {len(commands)} commands for device with ID {device_id}")

        return commands
