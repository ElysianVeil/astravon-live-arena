"""
============================================================
Astravon Live Arena
Alert Schemas

Purpose:
    Pydantic schemas for alert management.

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
# Alert Create Request
# ============================================================

class AlertCreateRequest(AstravonSchema):
    """
    Request schema for creating an alert.
    """

    title: str = Field(
        min_length=3,
        max_length=150
    )

    description: str = Field(
        min_length=5,
        max_length=1000
    )

    category: str = Field(
        default="General",
        max_length=50
    )

    severity: str = Field(
        default="Low",
        max_length=20
    )

    event_name: Optional[str] = None

    zone: Optional[str] = None

    risk_score: int = Field(
        default=0,
        ge=0,
        le=100
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )


# ============================================================
# Alert Update Request
# ============================================================

class AlertUpdateRequest(AstravonSchema):
    """
    Request schema for updating an alert.
    """

    title: Optional[str] = None

    description: Optional[str] = None

    category: Optional[str] = None

    severity: Optional[str] = None

    status: Optional[str] = None

    acknowledged: Optional[bool] = None

    resolved: Optional[bool] = None


# ============================================================
# Alert Data
# ============================================================

class AlertData(AstravonSchema):
    """
    Alert response payload.
    """

    id: int

    title: str

    description: str

    category: str

    severity: str

    event_name: Optional[str] = None

    zone: Optional[str] = None

    risk_score: int

    confidence: float

    status: str

    acknowledged: bool

    resolved: bool

    created_at: datetime

    acknowledged_at: Optional[datetime] = None

    resolved_at: Optional[datetime] = None


# ============================================================
# Alert Response
# ============================================================

class AlertResponse(
    SuccessResponse
):
    """
    Single alert response.
    """

    data: Optional[AlertData] = None


# ============================================================
# Alert List Response
# ============================================================

class AlertListResponse(
    SuccessResponse
):
    """
    Multiple alerts response.
    """

    data: List[AlertData] = []


# ============================================================
# Alert Statistics
# ============================================================

class AlertStatistics(AstravonSchema):
    """
    Alert statistics.
    """

    total: int

    active: int

    resolved: int

    critical: int

    high: int

    medium: int

    low: int


# ============================================================
# Alert Statistics Response
# ============================================================

class AlertStatisticsResponse(
    SuccessResponse
):
    """
    Alert statistics response.
    """

    data: Optional[AlertStatistics] = None