from domain.metric.model import Metric

from quanta_client.models.metric import Metric as ApiMetric

def convert_to_api(metric: Metric) -> ApiMetric:
    return ApiMetric(id=metric.id, name=metric.name, data_type=metric.type_name)
