from adapters.controller.device_controller import RestDeviceController
from adapters.controller.metrics_controller import MockMetricController
from adapters.controller.message_controller import MockMessageController

from domain.device.service import DeviceService
from adapters.repository.SQLAlchemy import SQLAlchemyDeviceRepository

device_service = DeviceService(SQLAlchemyDeviceRepository())
device = RestDeviceController(device_service)

metric = MockMetricController()
message = MockMessageController()
