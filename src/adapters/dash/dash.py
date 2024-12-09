from typing import Type
import dash
from dash import dcc, html
from flask import Flask
import logging

from config.config import config
import plotly.graph_objects as go

from adapters.dash.layout import html_layout

logger = logging.getLogger(__name__)
config.logging.configure_logger(logger)

from adapters.controller.controller import message_service

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
            go.Line(x=[message.datetime for message in messages], y=[get_type("float")(message.value) for message in messages], name="Trace 1"),
        ],
    )

    # Create Layout
    dash_module.layout = html.Div(
        children=[
            dcc.Graph(
                id="example-graph",
                figure=fig
                ),
        ],
        id="dash-container",
    )
    return dash_module.server

