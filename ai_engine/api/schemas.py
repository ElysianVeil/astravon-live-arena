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

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

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
# Crowd Statistics
# ============================================================

class StatisticsRequest(AstravonSchema):
    """
    Statistics submission request.
    """

    camera_id: str

    camera_name: str

    venue: str

    city: str

    country: str

    latitude: float

    longitude: float

    people_count: int = Field(
        ge=0
    )

    occupancy: float

    density: str

    temperature: float

    humidity: float

    heat_index: float

    wind_speed: float = Field(
        ge=0
    )

    weather_code: int

    city: str

    country: str

    risk_score: int = Field(
        ge=0,
        le=100
    )

    risk_level: str

    detected_objects: int = Field(
        ge=0
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    processing_time: float = Field(
        ge=0
    )

    fps: float = Field(
        ge=0
    )


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