import logging

from adapters.database.SQLAlchemy import Command as SQLAlchemyCommand, SessionLocal

from domain.command.model import Command
from domain.command.repository import CommandRepository

logger = logging.getLogger(__name__)

class SQLAlchemyCommandRepository(CommandRepository):

    def add(self, device_id: int, command: str) -> Command:
        logger.info(f"Adding command {command} to device with ID {device_id}")
        with SessionLocal() as db:
            new_command = SQLAlchemyCommand(device_id=device_id, command=command)
            db.add(new_command)
            db.commit()

            if new_command is None:
                raise ValueError(f"Command with device ID {device_id} and command {command} not found, command creation failed")

            logger.info(f"Command with device ID {new_command.device_id} and command {new_command.command} added, ID: {new_command.id}")

            return Command(new_command.device, new_command.command) # type: ignore

    def read_by_device_id(self, device_id: int) -> list[str]:
        logger.info(f"Getting all commands for device with ID {device_id}")
        with SessionLocal() as db:
            orm_commands = db.query(SQLAlchemyCommand) \
                .filter(
                        SQLAlchemyCommand.device_id == device_id, 
                        SQLAlchemyCommand.read == False) \
                .all()
            commands = [orm_command.command for orm_command in orm_commands]
            for orm_command in orm_commands:
                orm_command.read = True # type: ignore
            db.commit()

        return commands # type: ignore
