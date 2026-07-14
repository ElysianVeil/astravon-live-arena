"""
============================================================
Astravon Live Arena
AI Engine Constants

Purpose:
    Defines constant values used throughout the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

# ============================================================
# Application
# ============================================================

APP_NAME = "Astravon Live Arena AI Engine"

VERSION = "1.0.0"

AUTHOR = "House of Astravon"


# ============================================================
# Detection Labels
# ============================================================

PERSON = "person"

VEHICLE = "vehicle"

BAG = "bag"

UNKNOWN = "unknown"


# ============================================================
# COCO Class IDs
# ============================================================

PERSON_CLASS_ID = 0

BICYCLE_CLASS_ID = 1

CAR_CLASS_ID = 2

MOTORCYCLE_CLASS_ID = 3

BUS_CLASS_ID = 5

TRAIN_CLASS_ID = 6

TRUCK_CLASS_ID = 7

BACKPACK_CLASS_ID = 24

HANDBAG_CLASS_ID = 26

SUITCASE_CLASS_ID = 28


# ============================================================
# Detection Status
# ============================================================

STATUS_DETECTED = "detected"

STATUS_TRACKED = "tracked"

STATUS_LOST = "lost"

STATUS_EXITED = "exited"


# ============================================================
# Crowd Density
# ============================================================

LOW_DENSITY = "Low"

MEDIUM_DENSITY = "Medium"

HIGH_DENSITY = "High"

CRITICAL_DENSITY = "Critical"


# ============================================================
# Risk Levels
# ============================================================

LOW_RISK = "Low"

MEDIUM_RISK = "Medium"

HIGH_RISK = "High"

CRITICAL_RISK = "Critical"


# ============================================================
# Alert Severity
# ============================================================

INFO = "info"

WARNING = "warning"

DANGER = "danger"

EMERGENCY = "emergency"


# ============================================================
# Event Status
# ============================================================

EVENT_PENDING = "Pending"

EVENT_ACTIVE = "Active"

EVENT_PAUSED = "Paused"

EVENT_COMPLETED = "Completed"

EVENT_CANCELLED = "Cancelled"


# ============================================================
# Camera Status
# ============================================================

CAMERA_ONLINE = "online"

CAMERA_OFFLINE = "offline"

CAMERA_DISCONNECTED = "disconnected"

CAMERA_ERROR = "error"

STREAM_RECONNECT_DELAY = 2

# ============================================================
# Camera Types
# ============================================================

USB_CAMERA = "usb"

IP_CAMERA = "ip"

RTSP_CAMERA = "rtsp"

VIDEO_FILE = "video"

IMAGE_FILE = "image"


# ============================================================
# WebSocket Message Types
# ============================================================

MESSAGE_STATISTICS = "statistics"

MESSAGE_ALERT = "alert"

MESSAGE_EVENT = "event"

MESSAGE_SYSTEM = "system"

MESSAGE_CAMERA = "camera"


# ============================================================
# API Status
# ============================================================

SUCCESS = "success"

FAILED = "failed"

ERROR = "error"


# ============================================================
# Heat Levels
# ============================================================

HEAT_NORMAL = "Normal"

HEAT_WARNING = "Warning"

HEAT_DANGER = "Danger"

HEAT_EXTREME = "Extreme"


# ============================================================
# Processing Pipeline
# ============================================================

PIPELINE_CAMERA = "camera"

PIPELINE_PREPROCESS = "preprocessing"

PIPELINE_DETECTION = "detection"

PIPELINE_TRACKING = "tracking"

PIPELINE_ANALYTICS = "analytics"

PIPELINE_OUTPUT = "output"


# ============================================================
# Supported File Extensions
# ============================================================

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

VIDEO_EXTENSIONS = (
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".wmv"
)


# ============================================================
# Default Colors (BGR for OpenCV)
# ============================================================

COLOR_GREEN = (0, 255, 0)

COLOR_RED = (0, 0, 255)

COLOR_BLUE = (255, 0, 0)

COLOR_TRACK = (255, 180, 0)

COLOR_CAMERA = (255, 255, 0)

COLOR_YELLOW = (0, 255, 255)

COLOR_WHITE = (255, 255, 255)

COLOR_BLACK = (0, 0, 0)

COLOR_ORANGE = (0, 165, 255)

COLOR_PURPLE = (255, 0, 255)

DEFAULT_ZONE_THICKNESS = 2


# ============================================================
# Fonts
# ============================================================

FONT_SCALE_SMALL = 0.5

FONT_SCALE_NORMAL = 0.7

FONT_SCALE_LARGE = 1.0

LINE_THICKNESS = 2


# ============================================================
# Default Window Names
# ============================================================

MAIN_WINDOW = "Astravon Live Arena"

DEBUG_WINDOW = "Debug"

CAMERA_WINDOW_PREFIX = "Camera"


# ============================================================
# Logging
# ============================================================

LOGGER_NAME = "astravon_ai"


# ============================================================
# Default Messages
# ============================================================

ENGINE_STARTED = "AI Engine started successfully."

ENGINE_STOPPED = "AI Engine stopped."

CAMERA_CONNECTED = "Camera connected."

CAMERA_DISCONNECTED_MSG = "Camera disconnected."

MODEL_LOADED = "YOLO model loaded."

TRACKER_STARTED = "Tracker initialized."

BACKEND_CONNECTED = "Backend connection established."

BACKEND_DISCONNECTED = "Backend connection lost."

NO_CAMERAS_AVAILABLE = "No camera sources available."

PROCESSING_STARTED = "Vision pipeline started."

PROCESSING_STOPPED = "Vision pipeline stopped."