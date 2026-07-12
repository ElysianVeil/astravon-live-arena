"""
============================================================
Astravon Live Arena
Constants

Purpose:
    Shared application constants.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

# ============================================================
# Application
# ============================================================

APP_NAME = "Astravon Live Arena"

APP_VERSION = "1.0.0"

API_VERSION = "v1"

DEFAULT_HOST = "0.0.0.0"

DEFAULT_PORT = 8000


# ============================================================
# Event Modes
# ============================================================

EVENT_MODE_FOOTBALL = "football"

EVENT_MODE_CONCERT = "concert"

EVENT_MODE_FESTIVAL = "festival"

EVENT_MODE_SIMULATION = "simulation"

SUPPORTED_EVENT_MODES = [
    EVENT_MODE_FOOTBALL,
    EVENT_MODE_CONCERT,
    EVENT_MODE_FESTIVAL,
    EVENT_MODE_SIMULATION
]


# ============================================================
# Event Status
# ============================================================

STATUS_SCHEDULED = "scheduled"

STATUS_ACTIVE = "active"

STATUS_PAUSED = "paused"

STATUS_COMPLETED = "completed"

STATUS_CANCELLED = "cancelled"


# ============================================================
# Crowd Density
# ============================================================

DENSITY_LOW = "Low"

DENSITY_MEDIUM = "Medium"

DENSITY_HIGH = "High"

DENSITY_CRITICAL = "Critical"

DENSITY_LEVELS = [

    DENSITY_LOW,

    DENSITY_MEDIUM,

    DENSITY_HIGH,

    DENSITY_CRITICAL

]


# ============================================================
# Risk Levels
# ============================================================

RISK_LOW = "Low"

RISK_MEDIUM = "Medium"

RISK_HIGH = "High"

RISK_CRITICAL = "Critical"

RISK_LEVELS = [

    RISK_LOW,

    RISK_MEDIUM,

    RISK_HIGH,

    RISK_CRITICAL

]


# ============================================================
# Alert Severity
# ============================================================

SEVERITY_LOW = "Low"

SEVERITY_MEDIUM = "Medium"

SEVERITY_HIGH = "High"

SEVERITY_CRITICAL = "Critical"


# ============================================================
# Alert Status
# ============================================================

ALERT_ACTIVE = "Active"

ALERT_ACKNOWLEDGED = "Acknowledged"

ALERT_RESOLVED = "Resolved"


# ============================================================
# Detection
# ============================================================

PERSON_CLASS = "person"

DEFAULT_CONFIDENCE = 0.50

MAX_CONFIDENCE = 1.0


# ============================================================
# Arena
# ============================================================

DEFAULT_EVENT_NAME = "Football Match"

DEFAULT_VENUE = "Arena A"

DEFAULT_CAPACITY = 500

MAX_CAPACITY = 10000

DEFAULT_OCCUPANCY = 0


# ============================================================
# Environment
# ============================================================

DEFAULT_TEMPERATURE = 25.0

DEFAULT_HUMIDITY = 50.0

DEFAULT_HEAT_INDEX = 27.0

# ============================================================
# Camera Engine
# ============================================================

DEFAULT_CAMERA_INDEX = 0

FRAME_WIDTH = 1280

FRAME_HEIGHT = 720

FPS = 30

# ============================================================
# AI Engine
# ============================================================

# DEFAULT_FPS = 30.0

DEFAULT_PROCESSING_TIME = 0.0

DEFAULT_RISK_SCORE = 0

LOW_DENSITY_THRESHOLD = 30

MEDIUM_DENSITY_THRESHOLD = 80

HIGH_DENSITY_THRESHOLD = 120


LOW_RISK_THRESHOLD = 30

MEDIUM_RISK_THRESHOLD = 60

HIGH_RISK_THRESHOLD = 80


# ============================================================
# Reports
# ============================================================

REPORT_EVENT_SUMMARY = "Event Summary"

REPORT_CROWD_ANALYSIS = "Crowd Analysis"

REPORT_SAFETY = "Safety Report"

REPORT_INCIDENT = "Incident Report"

REPORT_AI = "AI Performance"


# ============================================================
# Vehicle Types
# ============================================================

VEHICLE_AMBULANCE = "Ambulance"

VEHICLE_SECURITY = "Security"

VEHICLE_FIRE = "Fire Engine"

VEHICLE_POLICE = "Police"

VEHICLE_EMERGENCY = "Emergency Vehicle"


# ============================================================
# WebSocket
# ============================================================

WEBSOCKET_PATH = "/ws"

WEBSOCKET_INTERVAL = 1


# ============================================================
# HTTP Messages
# ============================================================

SUCCESS_MESSAGE = "Operation completed successfully."

ERROR_MESSAGE = "Operation failed."

NOT_FOUND_MESSAGE = "Resource not found."

VALIDATION_MESSAGE = "Validation failed."

SERVER_ERROR_MESSAGE = "Internal Server Error."


# ============================================================
# Health Check
# ============================================================

HEALTH_STATUS = "Healthy"


# ============================================================
# Routes
# ============================================================

DEFAULT_ROUTE_STATUS = "Optimal"

DEFAULT_ROUTE_DISTANCE = "0 m"

DEFAULT_ROUTE_DURATION = "0 sec"