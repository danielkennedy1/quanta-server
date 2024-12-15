from dataclasses import dataclass

from domain.device.model import Device

@dataclass
class Command:
    device: Device
    command: str
