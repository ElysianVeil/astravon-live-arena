"""
============================================================
Astravon Live Arena
Statistics Schemas

Purpose:
    Pydantic schemas for crowd statistics.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from backend.schemas.common import (
    AstravonSchema,
    SuccessResponse
)


# ============================================================
# Statistics Request
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
# Statistics Data
# ============================================================

class StatisticsData(AstravonSchema):
    """
    Statistics response payload.
    """

    id: int

    camera_id: str

    camera_name: str

    venue: str

    city: str

    country: str

    latitude: float

    longitude: float

    people_count: int

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

    risk_score: int

    risk_level: str

    detected_objects: int

    confidence: float

    processing_time: float

    fps: float

    created_at: datetime


# ============================================================
# Statistics Summary
# ============================================================

class StatisticsSummary(AstravonSchema):
    """
    Dashboard summary.
    """

    total_records: int

    highest_people_count: int

    average_temperature: float

    highest_risk_score: int

    active_alerts: int


# ============================================================
# Statistics Response
# ============================================================

class StatisticsResponse(
    SuccessResponse
):
    """
    Single statistics response.
    """

    data: Optional[StatisticsData] = None


# ============================================================
# Statistics History Response
# ============================================================

class StatisticsHistoryResponse(
    SuccessResponse
):
    """
    Historical statistics response.
    """

    data: List[StatisticsData] = Field(default_factory=list)


# ============================================================
# Statistics Summary Response
# ============================================================

class StatisticsSummaryResponse(
    SuccessResponse
):
    """
    Statistics summary response.
    """

    data: Optional[StatisticsSummary] = None