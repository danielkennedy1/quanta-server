from domain.device.service import DeviceService
from adapters.repository.SQLAlchemyDeviceRepository import SQLAlchemyDeviceRepository
from adapters.controller.device_controller import RestDeviceController

device_service = DeviceService(SQLAlchemyDeviceRepository())
device = RestDeviceController(device_service)



from domain.metric.service import MetricService
from adapters.repository.SQLAlchemyMetricRepository import SQLAlchemyMetricRepository
from adapters.controller.metric_controller import RestMetricController

metric_service = MetricService(SQLAlchemyMetricRepository())
metric = RestMetricController(metric_service)



from domain.message.service import MessageService
from adapters.repository.SQLAlchemyMessageRepository import SQLAlchemyMessageRepository
from adapters.controller.message_controller import RestMessageController

message_service = MessageService(SQLAlchemyMessageRepository(), SQLAlchemyDeviceRepository(), SQLAlchemyMetricRepository())
message = RestMessageController(message_service)



from domain.command.service import CommandService
from adapters.repository.SQLAlchemyCommandRepository import SQLAlchemyCommandRepository
from adapters.controller.command_controller import RestCommandController

command_service = CommandService(SQLAlchemyDeviceRepository(), SQLAlchemyCommandRepository())
command = RestCommandController(command_service)

