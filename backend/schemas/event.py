"""
============================================================
Astravon Live Arena
Event Schemas

Purpose:
    Pydantic schemas for event management.

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
# Event Create Request
# ============================================================

class EventCreateRequest(AstravonSchema):
    """
    Request schema for creating an event.
    """

    name: str = Field(
        min_length=3,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    category: str = Field(
        default="Football",
        max_length=50
    )

    venue: str = Field(
        min_length=2,
        max_length=100
    )

    mode: str = Field(
        default="football",
        max_length=30
    )

    capacity: int = Field(
        ge=1,
        default=500
    )


# ============================================================
# Event Update Request
# ============================================================

class EventUpdateRequest(AstravonSchema):
    """
    Request schema for updating an event.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    category: Optional[str] = None

    venue: Optional[str] = None

    mode: Optional[str] = None

    capacity: Optional[int] = Field(
        default=None,
        ge=1
    )

    status: Optional[str] = None

    is_active: Optional[bool] = None


# ============================================================
# Event Data
# ============================================================

class EventData(AstravonSchema):
    """
    Event response data.
    """

    id: int

    name: str

    description: Optional[str] = None

    category: str

    venue: str

    mode: str

    capacity: int

    current_attendance: int

    status: str

    is_active: bool

    temperature: float

    humidity: float

    risk_level: str

    created_at: datetime

    updated_at: datetime


# ============================================================
# Event Response
# ============================================================

class EventResponse(SuccessResponse):
    """
    Single event response.
    """

    data: Optional[EventData] = None


# ============================================================
# Event List Response
# ============================================================

class EventListResponse(SuccessResponse):
    """
    Multiple events response.
    """

    data: List[EventData] = []


# ============================================================
# Event Status Response
# ============================================================

class EventStatusResponse(SuccessResponse):
    """
    Current event status.
    """

    data: Optional[dict] = None