from typing import List

import logging

from domain.metric.repository import MetricRepository
from domain.metric.model import Metric

from adapters.database.SQLAlchemy import Metric as SQLAlchemyMetric, SessionLocal

logger = logging.getLogger(__name__)

class SQLAlchemyMetricRepository(MetricRepository):
    def add(self, name, type_name) -> Metric:
        logger.info(f"Adding metric with name: {name} and type: {type_name}")
        with SessionLocal() as db:
            new_metric = SQLAlchemyMetric(name=name, type_name=type_name)
            db.add(new_metric)
            db.commit()
            
            if new_metric is None:
                raise ValueError(f"Metric with name {name} and type {type_name} not found, metric creation failed")

            logger.info(f"Metric with name {new_metric.name} and type {new_metric.type_name} added, ID: {new_metric.id}")

            return Metric(new_metric.id, new_metric.name, new_metric.type_name) # type: ignore

    def get(self, metric_id) -> Metric | None:
        logger.info(f"Getting metric with ID: {metric_id}")
        with SessionLocal() as db:
            orm_metric = db.query(SQLAlchemyMetric).filter(SQLAlchemyMetric.id == metric_id).first()

        if orm_metric is None:
            return None

        return Metric(orm_metric.id, orm_metric.name, orm_metric.type_name) # type: ignore

    def get_all(self) -> List[Metric]:
        logger.info("Getting all metrics")
        with SessionLocal() as db:
            orm_metrics = db.query(SQLAlchemyMetric).all()

        return [Metric(orm_metric.id, orm_metric.name, orm_metric.type_name) for orm_metric in orm_metrics] # type: ignore

    def delete(self, metric_id) -> Metric:
        logger.info(f"Deleting metric with ID: {metric_id}")
        with SessionLocal() as db:
            orm_metric = db.query(SQLAlchemyMetric).filter(SQLAlchemyMetric.id == metric_id).first()

            if orm_metric is None:
                raise ValueError(f"Metric with ID {metric_id} not found")

            db.delete(orm_metric)
            db.commit()

            logger.info(f"Metric with ID {metric_id} deleted")

        return Metric(orm_metric.id, orm_metric.name, orm_metric.type_name) # type: ignore

