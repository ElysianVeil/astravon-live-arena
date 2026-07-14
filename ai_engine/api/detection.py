"""
============================================================
Astravon Live Arena
Detection Schemas

Purpose:
    Pydantic schemas for AI detection requests
    and responses.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from api.common import (
    AstravonSchema,
    SuccessResponse
)


# ============================================================
# Detected Object
# ============================================================

class DetectedObject(AstravonSchema):
    """
    Represents one detected object.
    """

    label: str

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    x: int

    y: int

    width: int

    height: int


# ============================================================
# Detection Request
# ============================================================

class DetectionRequest(AstravonSchema):
    """
    AI Engine detection payload.
    """

    people_count: int = Field(
        ge=0
    )

    detected_objects: int = Field(
        ge=0
    )

    density: str

    occupancy: int = Field(
        ge=0
    )

    temperature: float

    humidity: float

    heat_index: float

    risk_score: int = Field(
        ge=0,
        le=100
    )

    risk_level: str

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    fps: float = Field(
        ge=0
    )

    processing_time: float = Field(
        ge=0
    )

    timestamp: datetime

    objects: List[DetectedObject] = []


# ============================================================
# Detection Data
# ============================================================

class DetectionData(AstravonSchema):
    """
    Detection response payload.
    """

    people_count: int

    density: str

    occupancy: int

    temperature: float

    humidity: float

    heat_index: float

    risk_score: int

    risk_level: str

    confidence: float

    fps: float

    processing_time: float

    timestamp: datetime


# ============================================================
# Detection Response
# ============================================================

class DetectionResponse(
    SuccessResponse
):
    """
    Detection API response.
    """

    data: Optional[DetectionData] = None