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
    AlertListResponse,
    AlertStatisticsResponse,
    # AlertDashboardResponse
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

    alerts = ai_service.current_alerts

    return AlertListResponse(
        success=True,
        message="Alerts retrieved successfully.",
        data=alerts
    )

# ============================================================
# Get Resolved Alerts
# ============================================================

@router.get(
    "/resolved",
    response_model=AlertListResponse,
    summary="Resolved Alerts"
)
async def get_resolved_alerts():

    alerts = ai_service.get_resolved_alerts()

    return AlertListResponse(

        success=True,

        message="Resolved alerts retrieved.",

        data=alerts

    )

# ============================================================
# Alert Dashboard
# ============================================================

# @router.get(
#     "/dashboard",
#     response_model=AlertDashboardResponse,
#     summary="Alert Dashboard"
# )
# async def dashboard():

#     return AlertDashboardResponse(

#         success=True,

#         message="Dashboard retrieved.",

#         data=ai_service.dashboard()

#     )

# ============================================================
# Critical Alerts
# ============================================================

@router.get(
    "/critical",
    response_model=AlertListResponse
)
async def critical_alerts():

    alerts = ai_service.get_critical_alerts()

    return AlertListResponse(

        success=True,

        message="Critical alerts.",

        data=alerts

    )

@router.get(
    "/warnings",
    response_model=AlertListResponse
)
async def warnings():

    return AlertListResponse(

        success=True,

        message="Warning alerts.",

        data=ai_service.get_warning_alerts()

    )

# ============================================================
# Search Alerts
# ============================================================

@router.get(
    "/search/{keyword}",
    response_model=AlertListResponse
)
async def search_alerts(
    keyword: str
):

    return AlertListResponse(

        success=True,

        message="Search completed.",

        data=ai_service.search_alerts(keyword)

    )

# ============================================================
# Archived Alerts
# ============================================================

@router.get(
    "/archive/{date}"
)
async def archive(

    date: str

):

    if ai_service.archive_storage is None:

        raise HTTPException(

            status_code=503,

            detail="Archive unavailable."

        )

    return {

        "success": True,

        "data": ai_service.archive_storage.load_alerts(

            date

        )

    }

# ============================================================
# Resolve All Alerts
# ============================================================

@router.put(
    "/resolve/all"
)
async def resolve_all():

    total = ai_service.resolve_all_alerts()

    return {

        "success": True,

        "message": f"{total} alerts resolved."

    }

# ============================================================
# Reset Alerts
# ============================================================

@router.post(
    "/reset"
)
async def reset():

    ai_service.reset_alerts()

    return {

        "success": True,

        "message": "Alerts reset."

    }

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

        "message": "Alert deleted.",

        "deleted_alert_id": alert_id

    }

# ============================================================
# Health
# ============================================================

@router.get("/health")
async def health():

    return {

        "status": "Healthy",

        "alerts":

            len(ai_service.get_alerts())

    }

# Future
#
# notification_service.broadcast_alert_update()
#
# whenever an alert changes.

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

    summary = {

        **ai_service.get_alert_statistics(),

        "current_alerts":

            len(

                ai_service.get_alerts()

            ),

        "critical":

            len(

                ai_service.get_critical_alerts()

            ),

        "warnings":

            len(

                ai_service.get_warning_alerts()

            )

    }


    return {
        "success": True,
        "message": "Alert statistics retrieved.",
        "data": summary
    }