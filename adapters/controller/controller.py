from datetime import datetime

# Device Functions
def getDevices():
    """Retrieve a list of all devices."""
    return [
        {"id": 1, "description": "Temperature Sensor in Room 101"},
        {"id": 2, "description": "Pressure Sensor in Room 202"}
    ]

def createDevice(device):
    """Register a new device."""
    return {"id": device.get("id", 3), "description": device.get("description", "Humidity Sensor in Room 103")}

def getDeviceById(id):
    """Retrieve a specific device by ID."""
    if id == 1:
        return {"id": 1, "description": "Temperature Sensor in Room 101"}
    return None  # Simulates a "not found" case

def deleteDevice(id):
    """Delete a specific device by ID."""
    return None  # Returns None to signify successful deletion


# Metric Functions
def getMetrics():
    """Retrieve a list of all metrics."""
    return [
        {"id": 1, "name": "Temperature", "data_type": "float"},
        {"id": 2, "name": "Humidity", "data_type": "integer"}
    ]

def createMetric(metric):
    """Register a new metric."""
    return {
        "id": metric.get("id", 3),
        "name": metric.get("name", "Pressure"),
        "data_type": metric.get("data_type", "float")
    }

def getMetricById(id):
    """Retrieve a specific metric by ID."""
    if id == 1:
        return {"id": 1, "name": "Temperature", "data_type": "float"}
    return None  # Simulates a "not found" case

def deleteMetric(id):
    """Delete a specific metric by ID."""
    return None  # Returns None to signify successful deletion


# Message Functions
def getMessages():
    """Retrieve a list of all messages."""
    return [
        {
            "id": 1,
            "device_id": 1,
            "metric_id": 1,
            "metric_value": "23.5",
            "timestamp": "2023-10-01T12:30:00Z"
        },
        {
            "id": 2,
            "device_id": 2,
            "metric_id": 2,
            "metric_value": "55",
            "timestamp": "2023-10-01T12:35:00Z"
        }
    ]

def createMessage(message):
    """Record a new message."""
    return {
        "id": message.get("id", 3),
        "device_id": message.get("device_id", 3),
        "metric_id": message.get("metric_id", 3),
        "metric_value": message.get("metric_value", "1013.25"),
        "timestamp": message.get("timestamp", datetime.utcnow().isoformat() + "Z")
    }

def getMessageById(id):
    """Retrieve a specific message by ID."""
    if id == 1:
        return {
            "id": 1,
            "device_id": 1,
            "metric_id": 1,
            "metric_value": "23.5",
            "timestamp": "2023-10-01T12:30:00Z"
        }
    return None  # Simulates a "not found" case

def deleteMessage(id):
    """Delete a specific message by ID."""
    return None  # Returns None to signify successful deletion
