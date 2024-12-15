from typing import Type
import dash
from dash import dcc, html, Input, Output
from flask import Flask
import logging

from config.config import config
import plotly.graph_objects as go

from adapters.dash.layout import html_layout

logger = logging.getLogger(__name__)
config.logging.configure_logger(logger)

from adapters.controller.controller import (
    metric_service,
    device_service,
    message_service,
)


def get_type(name: str) -> Type:
    """
    Retrieve a class by name.

    :param str name: Name of the class to retrieve.
    :return: Class type.
    """
    return {
        "float": float,
    }.get(name, str)


def init_dashboard(app: Flask):
    dash_module = dash.Dash(
        server=app,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    dash_module.index_string = html_layout
    dash_module.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Select a Device:"),
                            dcc.Dropdown(
                                id="device-selector",
                                options=[
                                    {"label": device.description, "value": device.id}
                                    for device in device_service.get_devices()
                                ],
                            ),
                            html.Label("Select a Metric:"),
                            dcc.Dropdown(
                                id="metric-selector",
                                options=[
                                    {"label": metric.name, "value": metric.id}
                                    for metric in metric_service.get_all()
                                ],
                            ),
                        ]
                    ),
                    dcc.Graph(id="gauge-chart", style={"width": "50%"}),
                ],
                style={"display": "flex", "flex-direction": "row", "justify-content": "space-between"},
            ),
            dcc.Graph(
                id="main-graph",
            ),
        ]
    )

    dash.callback(
        [Output("main-graph", "figure"), Output("gauge-chart", "figure")],
        [Input("device-selector", "value"), Input("metric-selector", "value")],
    )(update_graph)

    return dash_module.server


def update_graph(device_id, metric_id):

    logger.info(f"Updating graph for device {device_id} and metric {metric_id}")

    device = device_service.get_device(device_id)

    if device is None:
        return go.Figure(), go.Figure()

    metric = metric_service.get(metric_id)

    if metric is None:
        return go.Figure(), go.Figure()

    messages = message_service.get_all(device_id, metric_id)

    values = [get_type(metric.type_name)(message.value) for message in messages]

    if len(messages) == 0:
        return go.Figure(), go.Figure()

    line = go.Figure(
        data=[
            go.Line(
                x=[message.datetime for message in messages],
                y=values,
                name=f"Metric {metric.name} for Device {device.description}",
            ),
        ],
    )

    gauge = go.Figure(
        data=[
            go.Indicator(
                mode="gauge+number",
                value=values[-1],
                title=f"Current {metric.name}",
                gauge={"axis": {"range": [min(values), max(values)]}},
            ),
        ],
        layout=go.Layout(
            title=f"Device {device.description} Metric {metric.name}",
        ),
    )

    return line, gauge
