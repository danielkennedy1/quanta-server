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



from adapters.controller.message_controller import MockMessageController
message = MockMessageController()
