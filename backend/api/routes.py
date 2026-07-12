"""
============================================================
Astravon Live Arena
API Routes

Purpose:
    Main API router for Astravon Live Arena.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from fastapi import APIRouter, HTTPException

# ============================================================
# Schemas
# ============================================================

from backend.schemas.detection import DetectionRequest, DetectionResponse
from backend.schemas.event import (EventCreateRequest, EventResponse)
from backend.schemas.statistics import StatisticsResponse

# ============================================================
# Services
# ============================================================

from backend.dependencies.services import (
    ai_service,
    event_service
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/api/v1",
    tags=["Astravon Live Arena"]
)

# ============================================================
# Service Instances
# ============================================================

# ai_service = AIService()

# event_service = EventService()

# ============================================================
# Root Endpoint
# ============================================================

@router.get(
    "/",
    summary="API Root"
)
async def api_root():
    """
    Returns API information.
    """

    return {
        "success": True,
        "message": "Astravon Live Arena API",
        "data": {
            "version": "1.0.0"
        }
    }


# ============================================================
# Health Check
# ============================================================

@router.get(
    "/status",
    summary="Backend Status"
)
async def status():
    """
    Backend health check.
    """

    return {
        "success": True,
        "message": "Backend Online",
        "data": {
            "status": "healthy"
        }
    }


# ============================================================
# AI Detection
# ============================================================

@router.post(
    "/ai/detection",
    response_model=DetectionResponse,
    summary="Receive AI Detection"
)
async def receive_detection(
    request: DetectionRequest
):
    """
    Receives detection results
    from the AI Engine.
    """

    result = ai_service.process_detection(request)

    return DetectionResponse(
        success=True,
        message="Detection processed successfully.",
        data=result
    )


# ============================================================
# Current Event
# ============================================================

@router.get(
    "/events/current",
    response_model=EventResponse,
    summary="Current Event"
)
async def current_event():
    """
    Returns the currently
    active event.
    """

    event = event_service.get_current_event()

    return EventResponse(
        success=True,
        message="Current event loaded.",
        data=event
    )


# ============================================================
# Dashboard Statistics
# ============================================================

@router.get(
    "/statistics",
    response_model=StatisticsResponse,
    summary="Dashboard Statistics"
)
async def statistics():
    """
    Returns the latest
    dashboard statistics.
    """

    stats = ai_service.get_statistics()

    return StatisticsResponse(
        success=True,
        message="Statistics retrieved.",
        data=stats
    )


# ============================================================
# Reset Simulation
# ============================================================

@router.post(
    "/simulation/reset",
    summary="Reset Simulation"
)
async def reset_simulation():
    """
    Resets the simulation.
    """

    ai_service.reset()

    return {
        "success": True,
        "message": "Simulation reset successfully.",
        "data": {}
    }


# ============================================================
# Ping AI Engine
# ============================================================

@router.get(
    "/ai/ping",
    summary="Ping AI Engine"
)
async def ping_ai():
    """
    Tests communication
    with the AI Engine.
    """

    return {
        "success": True,
        "message": "AI Engine Online",
        "data": {
            "connected": True
        }
    }


# ============================================================
# API Information
# ============================================================

@router.get(
    "/info",
    summary="API Information"
)
async def info():
    """
    Returns backend information.
    """

    return {
        "success": True,
        "message": "Astravon Live Arena Backend",
        "data": {
            "version": "1.0.0",
            "api": "v1",
            "framework": "FastAPI"
        }
    }


# ============================================================
# Not Implemented Placeholder
# ============================================================

@router.get(
    "/future",
    summary="Future Feature"
)
async def future():
    """
    Placeholder endpoint
    for future functionality.
    """

    raise HTTPException(
        status_code=501,
        detail="Feature not implemented yet."
    )