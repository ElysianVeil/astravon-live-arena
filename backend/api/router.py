"""
============================================================
Astravon Live Arena
API Router Registry

Purpose:
    Registers all application routers.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from fastapi import APIRouter


# Core API
from backend.api.routes import router as core_router


# Feature APIs
from backend.api.alerts import router as alert_router
from backend.api.statistics import router as statistics_router
from backend.api.reports import router as report_router
from backend.api.websocket import router as websocket_router


# Emergency Routes API
from backend.api.emergency_routes.routes import router as emergency_route_router



# ============================================================
# Main API Router
# ============================================================

api_router = APIRouter()



# ============================================================
# Register Routers
# ============================================================


api_router.include_router(
    core_router
)


api_router.include_router(
    alert_router
)


api_router.include_router(
    statistics_router
)


api_router.include_router(
    report_router
)


api_router.include_router(
    emergency_route_router
)


api_router.include_router(
    websocket_router
)