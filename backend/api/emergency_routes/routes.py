from fastapi import APIRouter

from backend.schemas.route import (
    RouteRequest,
    RouteResponse
)

from backend.dependencies.services import route_service


router = APIRouter(
    prefix="/api/v1/routes",
    tags=["Routes"]
)


@router.post("/")
async def calculate_route(
    request: RouteRequest
):

    result = route_service.calculate_route(
        request.incident_location,
        request.destination
    )

    return {
        "success": True,
        "message": "Route calculated.",
        "data": result
    }


@router.get("/")
async def get_routes():

    return {
        "success": True,
        "message": "Routes retrieved.",
        "data": route_service.get_routes()
    }