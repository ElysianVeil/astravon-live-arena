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
from typing import List, Optional, Dict, Any

from pydantic import Field

from backend.schemas.common import (
    AstravonSchema,
    SuccessResponse
)


# ============================================================
# Statistics Request
# ============================================================

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
# Statistics Data
# ============================================================

class StatisticsData(AstravonSchema):
    """
    Statistics response payload.
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