"""
============================================================
Astravon Live Arena
Risk Thresholds

Purpose:
    Defines configurable thresholds used by the
    Risk Analysis Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from dataclasses import dataclass


# ============================================================
# Crowd Thresholds
# ============================================================

@dataclass(frozen=True)
class CrowdThresholds:
    """
    Crowd-related thresholds.
    """

    FREE_FLOW = 20

    LOW_DENSITY = 40

    MEDIUM_DENSITY = 70

    HIGH_DENSITY = 100

    CRITICAL_DENSITY = 140

    FREE_FLOW = 20

    LOW_DENSITY = 40

    MEDIUM_DENSITY = 70

    HIGH_DENSITY = 100

    CRITICAL_DENSITY = 140


# ============================================================
# Heat Thresholds
# ============================================================

@dataclass(frozen=True)
class HeatThresholds:
    """
    Heat index thresholds (°C).
    """

    SAFE: float = 27.0
    CAUTION: float = 32.0
    DANGER: float = 41.0
    EXTREME_DANGER: float = 54.0

# ============================================================
# Weather Thresholds
# ============================================================

@dataclass(frozen=True)
class WeatherThresholds:
    """
    Weather-related thresholds.
    """

    HIGH_HUMIDITY: float = 75.0

    LOW_HUMIDITY: float = 25.0

    HIGH_WIND: float = 30.0

    STORM_WIND: float = 45.0

    HIGH_UV: int = 8

    EXTREME_UV: int = 11

    LOW_PRESSURE: float = 1000.0

    HIGH_PRESSURE: float = 1025.0

    RAIN_PROBABILITY: int = 60

# ============================================================
# Heatstroke Thresholds
# ============================================================

@dataclass(frozen=True)
class HeatstrokeThresholds:

    LOW: int = 20

    MODERATE: int = 40

    HIGH: int = 60

    CRITICAL: int = 80

# ============================================================
# Stampede Thresholds
# ============================================================

@dataclass(frozen=True)
class StampedeThresholds:

    LOW_SPEED = 1.0

    MODERATE_SPEED = 2.5

    HIGH_SPEED = 4.5

    PANIC_SPEED = 7.0


# ============================================================
# Risk Score Thresholds
# ============================================================

@dataclass(frozen=True)
class RiskThresholds:
    """
    Overall risk score thresholds.
    """
    SAFE = 20

    MONITOR = 40

    WARNING = 60

    HIGH = 75

    DANGER = 90

    CRITICAL = 100

# ============================================================
# Prediction Thresholds
# ============================================================

@dataclass(frozen=True)
class PredictionThresholds:

    HISTORY_REQUIRED = 5

    MAX_FORECAST_MINUTES = 30

    TREND_STABLE = 2

    TREND_RISING = 5

    TREND_FALLING = -5

# ============================================================
# Camera Thresholds
# ============================================================

@dataclass(frozen=True)
class CameraThresholds:

    MINIMUM_FPS = 15

    TARGET_FPS = 30

    MAX_PROCESSING_TIME = 0.1

    MAX_FRAME_DELAY = 0.5

# ============================================================
# Backend Thresholds
# ============================================================

@dataclass(frozen=True)
class BackendThresholds:

    WEBSOCKET_TIMEOUT = 10

    HTTP_TIMEOUT = 5

    MAX_QUEUE_SIZE = 500

# ============================================================
# Analytics Thresholds
# ============================================================

@dataclass(frozen=True)
class AnalyticsThresholds:

    MAX_LOG_HISTORY = 1000

    MAX_EVENTS = 5000

    REPORT_INTERVAL = 300


# ============================================================
# Alert Timing
# ============================================================

@dataclass(frozen=True)
class AlertTiming:

    WARNING_COOLDOWN = 30

    CRITICAL_COOLDOWN = 10

    EMERGENCY_COOLDOWN = 5

# ============================================================
# Dashboard
# ============================================================

@dataclass(frozen=True)
class DashboardThresholds:

    GRAPH_HISTORY = 200

    MAP_HISTORY = 100

    ALERT_HISTORY = 100

# ============================================================
# Simulation
# ============================================================

@dataclass(frozen=True)
class SimulationThresholds:

    MIN_SPEED = 0.5

    DEFAULT_SPEED = 1.0

    MAX_SPEED = 10.0

# ============================================================
# Engine
# ============================================================

@dataclass(frozen=True)
class EngineThresholds:

    MAX_TRACKS = 5000

    MAX_DETECTIONS = 5000

    FRAME_BUFFER = 100

# ============================================================
# Severity Colors
# ============================================================

@dataclass(frozen=True)
class SeverityColors:

    SAFE = "#2ECC71"

    MONITOR = "#F1C40F"

    WARNING = "#F39C12"

    DANGER = "#E67E22"

    CRITICAL = "#E74C3C"

# ============================================================
# Severity Icons
# ============================================================

@dataclass(frozen=True)
class SeverityIcons:

    SAFE = "🟢"

    WARNING = "🟡"

    DANGER = "🟠"

    CRITICAL = "🔴"

# ============================================================
# Threshold Metadata
# ============================================================

THRESHOLD_INFO = {

    "module": "Risk Thresholds",

    "version": "2.0.0",

    "description": "Centralized thresholds for Astravon Live Arena",

    "author": "House of Astravon"
}

# ============================================================
# Crowd Movement Thresholds
# ============================================================

@dataclass(frozen=True)
class MovementThresholds:
    """
    Crowd movement speed (pixels/frame or normalized units).
    """

    SLOW: float = 1.5
    NORMAL: float = 3.0
    FAST: float = 5.0


# ============================================================
# Congestion Thresholds
# ============================================================

@dataclass(frozen=True)
class CongestionThresholds:
    """
    Congestion ratio thresholds.
    """

    LOW: float = 0.30
    MEDIUM: float = 0.60
    HIGH: float = 0.85


# ============================================================
# Alert Thresholds
# ============================================================

@dataclass(frozen=True)
class AlertThresholds:
    """
    Automatic alert generation thresholds.
    """

    PEOPLE_WARNING: int = 250
    PEOPLE_CRITICAL: int = 500

    TEMPERATURE_WARNING: float = 32.0
    TEMPERATURE_CRITICAL: float = 38.0

    RISK_WARNING: int = 60
    RISK_CRITICAL: int = 85


# ============================================================
# Export Singleton Instances
# ============================================================

CROWD = CrowdThresholds()

HEAT = HeatThresholds()

RISK = RiskThresholds()

MOVEMENT = MovementThresholds()

CONGESTION = CongestionThresholds()

ALERTS = AlertThresholds()

WEATHER = WeatherThresholds()

HEATSTROKE = HeatstrokeThresholds()

STAMPEDE = StampedeThresholds()

PREDICTION = PredictionThresholds()

CAMERA = CameraThresholds()

BACKEND = BackendThresholds()

ANALYTICS = AnalyticsThresholds()

ALERT_TIMING = AlertTiming()

DASHBOARD = DashboardThresholds()

SIMULATION = SimulationThresholds()

ENGINE = EngineThresholds()

COLORS = SeverityColors()

ICONS = SeverityIcons()