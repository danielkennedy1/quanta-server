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
    """
    Create a Plotly Dash dashboard within a running Flask app.

    :param Flask app: Top-level Flask application.
    """
    dash_module = dash.Dash(
        server=app,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Custom HTML layout
    dash_module.index_string = html_layout

    messages = message_service.get_all(device_id=1, metric_id=1)

    fig = go.Figure(
        data=[
            go.Line(
                x=[message.datetime for message in messages],
                y=[get_type("float")(message.value) for message in messages],
                name="Trace 1",
            ),
        ],
    )

    # Create Layout
    dash_module.layout = html.Div(
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
                        style={"width": "50%"},
                    ),
                    html.Label("Select a Metric:"),
                    dcc.Dropdown(
                        id="metric-selector",
                        options=[
                            {"label": metric.name, "value": metric.id}
                            for metric in metric_service.get_all()
                        ],
                        style={"width": "50%"},
                    ),
                ]
            ),
            dcc.Graph(
                id="main-graph",
            ),
        ]
    )

    dash.callback(
        Output("main-graph", "figure"),
        [Input("device-selector", "value"), Input("metric-selector", "value")],
    )(update_graph)

    return dash_module.server


def update_graph(device_id, metric_id):

    logger.info(f"Updating graph for device {device_id} and metric {metric_id}")

    device = device_service.get_device(device_id)

    if device is None:
        return go.Figure()

    metric = metric_service.get(metric_id)

    if metric is None:
        return go.Figure()

    messages = message_service.get_all(device_id, metric_id)

    if len(messages) == 0:
        return go.Figure()

    fig = go.Figure(
        data=[
            go.Line(
                x=[message.datetime for message in messages],
                y=[get_type(metric.type_name)(message.value) for message in messages],
                name=f"Metric {metric.name} for Device {device.description}",
            ),
        ],
    )

    return fig
