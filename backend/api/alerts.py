"""
============================================================
Astravon Live Arena
Alert API

Purpose:
    Handles alert-related endpoints.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.alert import (
    AlertCreateRequest,
    AlertResponse,
    AlertListResponse
)

from backend.dependencies.services import ai_service

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["Alerts"]
)

# ============================================================
# Services
# ============================================================

# ai_service = AIService()

# ============================================================
# Get Active Alerts
# ============================================================

@router.get(
    "/",
    response_model=AlertListResponse,
    summary="Get Active Alerts"
)
async def get_alerts():
    """
    Returns all active alerts.
    """

    alerts = ai_service.get_alerts()

    return AlertListResponse(
        success=True,
        message="Alerts retrieved successfully.",
        data=alerts
    )

# ============================================================
# Create Alert
# ============================================================

@router.post(
    "/",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Alert"
)
async def create_alert(
    request: AlertCreateRequest
):
    """
    Creates a new alert.
    """

    alert = ai_service.create_alert(request)

    return AlertResponse(
        success=True,
        message="Alert created successfully.",
        data=alert
    )

# ============================================================
# Get Alert
# ============================================================

@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
    summary="Get Alert"
)
async def get_alert(
    alert_id: int
):
    """
    Returns one alert.
    """

    alert = ai_service.get_alert(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found."
        )

    return AlertResponse(
        success=True,
        message="Alert retrieved successfully.",
        data=alert
    )

# ============================================================
# Resolve Alert
# ============================================================

@router.put(
    "/{alert_id}/resolve",
    response_model=AlertResponse,
    summary="Resolve Alert"
)
async def resolve_alert(
    alert_id: int
):
    """
    Marks an alert as resolved.
    """

    alert = ai_service.resolve_alert(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found."
        )

    return AlertResponse(
        success=True,
        message="Alert resolved successfully.",
        data=alert
    )

# ============================================================
# Delete Alert
# ============================================================

@router.delete(
    "/{alert_id}",
    summary="Delete Alert"
)
async def delete_alert(
    alert_id: int
):
    """
    Deletes an alert.
    """

    deleted = ai_service.delete_alert(alert_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found."
        )

    return {
        "success": True,
        "message": "Alert deleted successfully.",
        "data": {}
    }

# ============================================================
# Alert Statistics
# ============================================================

@router.get(
    "/statistics/summary",
    summary="Alert Summary"
)
async def alert_summary():
    """
    Returns alert statistics.
    """

    summary = ai_service.get_alert_statistics()

    return {
        "success": True,
        "message": "Alert statistics retrieved.",
        "data": summary
    }