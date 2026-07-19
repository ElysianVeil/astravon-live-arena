"""
============================================================
Astravon Live Arena
Statistics API

Purpose:
    Handles crowd statistics endpoints.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.statistics import (
    StatisticsRequest,
    StatisticsResponse,
    StatisticsHistoryResponse,
)

from backend.dependencies.services import ai_service

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/api/v1/statistics",
    tags=["Statistics"]
)

# ============================================================
# Services
# ============================================================

# ai_service = AIService()

# ============================================================
# Current Statistics
# ============================================================

@router.get(
    "/",
    response_model=StatisticsResponse,
    summary="Current Statistics"
)
async def get_statistics():
    """
    Returns the latest statistics from
    the AI Engine.
    """

    statistics = ai_service.get_statistics()

    return StatisticsResponse(
        success=True,
        message="Statistics retrieved successfully.",
        data=statistics
    )


# ============================================================
# Submit Statistics
# ============================================================

@router.post(
    "/",
    response_model=StatisticsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Statistics"
)
async def create_statistics(
    request: StatisticsRequest
):
    """
    Receives statistics from
    the AI Engine.
    """

    statistics = ai_service.save_statistics(request)

    return StatisticsResponse(
        success=True,
        message="Statistics saved successfully.",
        data=statistics
    )


@router.post(
    "/weather",
    summary="Weather Statistics"
)
async def weather():

    return {

        "success": True,

        "message": "Weather retrieved.",

        "data": ai_service.get_weather()

    }

@router.get(
    "/density"
)
async def density():

    return {

        "success": True,

        "message": "Density retrieved.",

        "data": ai_service.get_density()

    }

@router.get(
    "/risk"
)
async def risk():

    return {

        "success": True,

        "message": "Risk retrieved.",

        "data": ai_service.get_risk()

    }

@router.get(
    "/occupancy"
)
async def occupancy():

    return {

        "success": True,

        "message": "Occupancy retrieved.",

        "data": ai_service.get_occupancy()

    }

@router.get(
    "/congestion"
)
async def congestion():

    return {

        "success": True,

        "message": "Congestion retrieved.",

        "data": ai_service.get_congestion()

    }

@router.get(
    "/detection"
)
async def detection():

    return {

        "success": True,

        "message": "Detection statistics.",

        "data": ai_service.get_detection()

    }

@router.get(
    "/camera"
)
async def camera():

    return {

        "success": True,

        "message": "Camera statistics.",

        "data": ai_service.get_camera()

    }

@router.get(
    "/performance"
)
async def performance():

    return {

        "success": True,

        "message": "Performance statistics.",

        "data": ai_service.get_performance()

    }

@router.get(
    "/engine"
)
async def engine():

    return {

        "success": True,

        "message": "Engine status.",

        "data": ai_service.get_engine()

    }


# ============================================================
# Statistics History
# ============================================================

@router.get(
    "/history",
    response_model=StatisticsHistoryResponse,
    summary="Statistics History"
)
async def statistics_history():
    """
    Returns historical statistics.
    """

    history = ai_service.get_statistics_history()

    return StatisticsHistoryResponse(
        success=True,
        message="Statistics history retrieved.",
        data=history
    )


# ============================================================
# Statistics Summary
# ============================================================

@router.get(
    "/summary",
    summary="Statistics Summary"
)
async def statistics_summary():
    """
    Returns aggregated statistics.
    """

    summary = ai_service.get_statistics_summary()

    return {
        "success": True,
        "message": "Summary generated successfully.",
        "data": summary
    }


# ============================================================
# Highest Crowd Count
# ============================================================

@router.get(
    "/highest",
    summary="Highest Crowd Count"
)
async def highest_crowd():
    """
    Returns the highest recorded crowd count.
    """

    highest = ai_service.get_highest_crowd()

    return {
        "success": True,
        "message": "Highest crowd count retrieved.",
        "data": highest
    }


# ============================================================
# Current Risk
# ============================================================

@router.get(
    "/risk",
    summary="Current Risk"
)
async def current_risk():
    """
    Returns the current calculated risk.
    """

    risk = ai_service.get_current_risk()

    return {
        "success": True,
        "message": "Current risk retrieved.",
        "data": risk
    }


# ============================================================
# Current Density
# ============================================================

@router.get(
    "/density",
    summary="Current Density"
)
async def current_density():
    """
    Returns the current crowd density.
    """

    density = ai_service.get_density()

    return {
        "success": True,
        "message": "Density retrieved.",
        "data": density
    }


# ============================================================
# Current Occupancy
# ============================================================

@router.get(
    "/occupancy",
    summary="Current Occupancy"
)
async def current_occupancy():
    """
    Returns the current venue occupancy.
    """

    occupancy = ai_service.get_occupancy()

    return {
        "success": True,
        "message": "Occupancy retrieved.",
        "data": occupancy
    }


# ============================================================
# Current Temperature
# ============================================================

@router.get(
    "/temperature",
    summary="Current Temperature"
)
async def current_temperature():
    """
    Returns the current simulated temperature.
    """

    temperature = ai_service.get_temperature()

    return {
        "success": True,
        "message": "Temperature retrieved.",
        "data": temperature
    }


# ============================================================
# Delete Statistics
# ============================================================

@router.delete(
    "/{statistics_id}",
    summary="Delete Statistics"
)
async def delete_statistics(
    statistics_id: int
):
    """
    Deletes a statistics record.
    """

    deleted = ai_service.delete_statistics(statistics_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics record not found."
        )

    return {
        "success": True,
        "message": "Statistics deleted successfully.",
        "data": {}
    }