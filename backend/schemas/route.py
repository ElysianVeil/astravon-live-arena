"""
============================================================
Astravon Live Arena
Route Schemas

Purpose:
    Pydantic schemas for emergency vehicle routing.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import List, Optional

from pydantic import Field

from backend.schemas.common import (
    AstravonSchema,
    SuccessResponse
)


# ============================================================
# Route Request
# ============================================================

class RouteRequest(AstravonSchema):
    """
    Request for calculating an emergency route.
    """

    incident_location: str = Field(
        min_length=2,
        max_length=100
    )

    destination: str = Field(
        min_length=2,
        max_length=100
    )

    vehicle_type: str = Field(
        default="Emergency Vehicle",
        max_length=50
    )

# ============================================================
# Route Lookup Request
# ============================================================

class RouteLookupRequest(AstravonSchema):
    """
    Request for retrieving an existing route.
    """

    route_id: int


# ============================================================
# Route Step
# ============================================================

class RouteStep(AstravonSchema):
    """
    Individual navigation instruction.
    """

    step: int

    instruction: str

    distance: str

    estimated_time: str


# ============================================================
# Route Data
# ============================================================

class RouteData(AstravonSchema):
    """
    Route information returned to the client.
    """

    start_location: str

    destination: str

    vehicle_type: str

    total_distance: str

    estimated_duration: str

    status: str

    steps: List[RouteStep]


# ============================================================
# Route Response
# ============================================================

class RouteResponse(
    SuccessResponse
):
    """
    Route calculation response.
    """

    data: Optional[RouteData] = None


# ============================================================
# Route History Item
# ============================================================

class RouteHistoryItem(AstravonSchema):
    """
    Previous emergency route.
    """

    id: int

    incident_location: str

    destination: str

    vehicle_type: str

    estimated_duration: str

    status: str


# ============================================================
# Route History Response
# ============================================================

class RouteHistoryResponse(
    SuccessResponse
):
    """
    Route history response.
    """

    data: List[RouteHistoryItem] = []


# ============================================================
# Route Summary
# ============================================================

class RouteSummary(AstravonSchema):
    """
    Routing statistics.
    """

    total_routes: int

    successful_routes: int

    average_response_time: str


# ============================================================
# Route Summary Response
# ============================================================

class RouteSummaryResponse(
    SuccessResponse
):
    """
    Route statistics response.
    """

    data: Optional[RouteSummary] = None