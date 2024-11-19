from domain.metric.model import Metric
from domain.message.model import Message

from quanta_client.models.metric import Metric as ApiMetric
from quanta_client.models.message import Message as ApiMessage


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
