from domain.metric.model import Metric
from domain.message.model import Message
from domain.command.model import Command

from quanta_client.models.metric import Metric as ApiMetric
from quanta_client.models.message import Message as ApiMessage
from quanta_client.models.command import Command as ApiCommand


def convert_metric_to_api(metric: Metric) -> ApiMetric:
    return ApiMetric(id=metric.id, name=metric.name, data_type=metric.type_name)


def convert_message_to_api(message: Message) -> ApiMessage:
    return ApiMessage(
        id=message.id,
        device_id=message.device.id,
        metric_id=message.metric.id,
        metric_value=message.value,
        timestamp=message.datetime.isoformat() + "Z",
    )

def convert_command_to_api(command: Command) -> ApiCommand:
    return ApiCommand(device_id=command.device.id, command=command.command)
