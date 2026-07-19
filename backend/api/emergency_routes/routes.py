from fastapi import APIRouter, HTTPException

from backend.schemas.route import (
    RouteRequest,
    RouteResponse
)

from backend.dependencies.services import route_service


router = APIRouter(
    prefix="/api/v1/routes",
    tags=["Routes"]
)


@router.post("/calculate")
async def calculate_route(
    request: RouteRequest
):
    # Future Implementation
    #
    # 1. Query OpenStreetMap
    #
    # 2. Build road graph
    #
    # 3. Run A* search
    #
    # 4. Estimate travel time
    #
    # 5. Factor traffic
    #
    # 6. Factor blocked roads
    #
    # 7. Return optimal route

    try:
        if request.incident_location == request.destination:

            raise HTTPException(

                status_code=400,

                detail="Origin and destination cannot match."

            )

        result = route_service.calculate_route(
            request.incident_location,
            request.destination
        )

        return RouteResponse(

            success=True,

            message="Route calculated.",

            data=result

        )

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )

    except Exception:

        raise HTTPException(

            status_code=500,

            detail="Unable to calculate route."

    )


@router.get("/")
async def get_routes():

    return {
        "success": True,
        "message": "Routes retrieved.",
        "data": route_service.get_routes()
    }

@router.get(
    "/{route_id}",
    response_model=RouteResponse,
    summary="Get Route"
)
async def get_route(
    route_id: int
):

    route = route_service.get_route(route_id)

    if route is None:

        raise HTTPException(
            status_code=404,
            detail="Route not found."
        )

    return RouteResponse(

        success=True,

        message="Route retrieved.",

        data=route

    )

@router.post(
    "/dispatch",
    summary="Dispatch Emergency Vehicle"
)
async def dispatch_vehicle(
    request: RouteRequest
):

    dispatch = route_service.dispatch_vehicle(

        request.vehicle_type,

        request.destination

    )

    return {

        "success": True,

        "message": "Vehicle dispatched.",

        "data": dispatch

    }

@router.get(
    "/recommended/{destination}",
    summary="Recommended Route"
)
async def recommended_route(
    destination: str
):

    route = route_service.recommended_route(
        destination
    )

    return {

        "success": True,

        "message":"Recommended route.",

        "data": route

    }

@router.get(
    "/statistics"
)
async def statistics():

    return {

        "success": True,

        "message":"Route statistics.",

        "data":

            route_service.get_statistics()

    }

@router.post(
    "/create"
)
async def create_route(
    request: RouteRequest
):

    route = route_service.create_route(
        request
    )

    return {

        "success":True,

        "message":"Route created.",

        "data":route

    }

@router.delete(
    "/{route_id}"
)
async def delete_route(
    route_id: int
):

    deleted = route_service.delete_route(
        route_id
    )

    if not deleted:

        raise HTTPException(

            status_code=404,

            detail="Route not found."

        )

    return {

        "success":True,

        "message":"Route deleted.",

        "data":{}

    }

@router.post(
    "/reset"
)
async def reset():

    route_service.reset()

    return {

        "success":True,

        "message":"Routes reset.",

        "data":{}

    }