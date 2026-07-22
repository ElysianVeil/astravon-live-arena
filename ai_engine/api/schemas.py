"""
============================================================
Astravon Live Arena
AI API Schemas

Purpose:
    Defines the data models exchanged between the
    AI Engine and the Backend API.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""



from datetime import datetime
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field
from api.common import AstravonSchema


# ============================================================
# Base Response
# ============================================================

class APIResponse(BaseModel):
    """
    Standard API response.
    """

    success: bool = True

    message: str = "Success"

    data: Dict = Field(default_factory=dict)


# ============================================================
# Detection
# ============================================================

class Detection(BaseModel):
    """
    Single object detection.
    """

    id: int

    label: str

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    x1: float

    y1: float

    x2: float

    y2: float

    camera_id: str = "camera_1"


class DetectionRequest(BaseModel):
    """
    Detection payload.
    """

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )

    detections: List[Detection]





# ============================================================
# Engine
# ============================================================

class EngineStatistics(AstravonSchema):

    name: str

    version: str

    status: str

    uptime: float

    generated_statistics: int


# ============================================================
# Detection
# ============================================================

class DetectionStatistics(AstravonSchema):

    people_count: int = Field(ge=0)

    detector: Dict[str, Any]


# ============================================================
# Performance
# ============================================================

class PerformanceStatistics(AstravonSchema):

    average_processing_time: float = Field(ge=0)

    processing_time: float = Field(ge=0)

    average_fps: float = Field(ge=0)

    current_fps: float = Field(ge=0)

    camera: Dict[str, Any]

    detector: Dict[str, Any]

    tracker: Dict[str, Any]

    movement: Dict[str, Any]

    feature_extractor: Dict[str, Any]

    identity_database: Dict[str, Any]

    matcher: Dict[str, Any]

    counter: Dict[str, Any]

    density: Dict[str, Any]

    occupancy: Dict[str, Any]

    congestion: Dict[str, Any]


# ============================================================
# Crowd Statistics
# ============================================================

class StatisticsRequest(AstravonSchema):
    """
    Complete crowd statistics payload.
    Mirrors CrowdStatistics.build().
    """

    timestamp: str

    statistics_version: str

    engine: EngineStatistics

    camera: Dict[str, Any]

    detection: DetectionStatistics

    movement: Dict[str, Any]

    density: Dict[str, Any]

    occupancy: Dict[str, Any]

    congestion: Dict[str, Any]

    risk: Optional[Dict[str, Any]] = None

    weather: Optional[Dict[str, Any]] = None

    trends: Optional[Dict[str, Any]] = None

    zones: Optional[Dict[str, Any]] = None

    performance: PerformanceStatistics


# ============================================================
# Alert
# ============================================================

class AlertRequest(BaseModel):
    """
    Emergency alert.
    """

    title: str

    severity: str

    description: str

    location: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


# ============================================================
# Route
# ============================================================

class RouteRequest(BaseModel):
    """
    Emergency route.
    """

    incident_location: str

    destination: str

    vehicle_type: str = "Emergency Vehicle"

    estimated_time: Optional[float] = None

    distance_km: Optional[float] = None


# ============================================================
# Report
# ============================================================

class ReportRequest(BaseModel):
    """
    Report payload.
    """

    event_name: str

    statistics: StatisticsRequest

    alerts: List[AlertRequest] = Field(
        default_factory=list
    )


# ============================================================
# Camera
# ============================================================

class CameraStatus(BaseModel):
    """
    Camera information.
    """

    camera_id: str

    name: str

    source: str

    connected: bool

    fps: float

    resolution: str


# ============================================================
# Health
# ============================================================

class HealthStatus(BaseModel):
    """
    AI Engine health.
    """

    status: str = "healthy"

    model_loaded: bool = True

    active_cameras: int = 0

    uptime_seconds: float = 0.0