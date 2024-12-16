from flask import render_template

from adapters.controller.controller import device_service

def index():
    devices = device_service.get_devices()

    return render_template('index.html', devices=devices)
