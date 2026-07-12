"""
============================================================
Astravon Live Arena
Route Service

Purpose:
    Handles emergency response route planning.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import Dict, List, Optional

from backend.utils.logger import get_logger
from backend.schemas.route import (RouteRequest, RouteLookupRequest)

from backend.utils.constants import (
    DEFAULT_ROUTE_STATUS,
    VEHICLE_EMERGENCY
)

class RouteService:
    """
    Business logic for emergency response routes.
    """

    logger = get_logger(
        "RouteService"
    )

    def __init__(self):

        self.routes: List[dict] = [
            {
                "id": 1,
                "vehicle": "Response Unit 1",
                "origin": "Emergency Station",
                "destination": "Zone A",
                "distance_km": 1.8,
                "estimated_time_min": 3,
                "status": DEFAULT_ROUTE_STATUS,
                "created_at": datetime.now().isoformat()
            }
        ]

    # ========================================================
    # Route Retrieval
    # ========================================================

    def get_routes(self) -> List[dict]:
        """
        Returns all available routes.
        """

        return self.routes

    def get_route(
        self,
        request: RouteLookupRequest
    ) -> Optional[dict]:
        """
        Returns a route by ID.
        """

        for route in self.routes:

            if route["id"] == request.route_id:
                return route

        return None

    # ========================================================
    # Route Planning
    # ========================================================

    def calculate_route(
        self,
        origin: str,
        destination: str
    ) -> Dict:
        """
        Simulates route planning.

        Future:
        - OpenStreetMap
        - Google Maps
        - Dijkstra
        - A* Search
        """

        route = {
            "origin": origin,
            "destination": destination,
            "distance_km": 2.4,
            "estimated_time_min": 5,
            "traffic": "Low",
            "status": "Ready"
        }

        return route

    # ========================================================
    # Dispatch
    # ========================================================

    def dispatch_vehicle(
        self,
        vehicle: str,
        destination: str
    ) -> Dict:
        """
        Dispatches a response vehicle.
        """
        self.logger.info(
            f"Dispatching vehicle {vehicle}"
        )

        dispatch = {
            "vehicle": vehicle,
            "destination": destination,
            "status": "Dispatched",
            "dispatch_time": datetime.now().isoformat()
        }

        return dispatch

    # ========================================================
    # Route Creation
    # ========================================================

    def create_route(
        self,
        request: RouteRequest
    ) -> Dict:
        """
        Creates a new emergency route.
        """

        route = {

            "id": len(self.routes) + 1,

            "vehicle": request.vehicle_type,

            "origin": request.incident_location,

            "destination": request.destination,

            "distance_km": 0,

            "estimated_time_min": 0,

            "status": "available",

            "created_at": datetime.now().isoformat()

        }

        self.routes.append(
            route
        )

        return route

    # ========================================================
    # Route Update
    # ========================================================

    def update_route(
        self,
        route_id: int,
        request
    ) -> Optional[Dict]:
        """
        Updates an existing route.
        """

        route = self.get_route(route_id)

        if route is None:
            return None

        route["vehicle"] = request.vehicle
        route["origin"] = request.origin
        route["destination"] = request.destination
        route["distance_km"] = request.distance_km
        route["estimated_time_min"] = request.estimated_time_min

        return route

    # ========================================================
    # Delete Route
    # ========================================================

    def delete_route(
        self,
        route_id: int
    ) -> bool:
        """
        Deletes a route.
        """

        route = self.get_route(route_id)

        if route:

            self.routes.remove(route)

            return True

        return False

    # ========================================================
    # Route Statistics
    # ========================================================

    def get_statistics(self) -> Dict:
        """
        Returns route statistics.
        """

        total = len(self.routes)

        available = len(
            [
                route
                for route in self.routes
                if route["status"] == "available"
            ]
        )

        return {
            "total_routes": total,
            "available_routes": available
        }

    # ========================================================
    # Recommended Route
    # ========================================================

    def recommended_route(
        self,
        destination: str
    ) -> Dict:
        """
        Returns the recommended route.
        """

        return {
            "vehicle": "Response Unit 1",
            "destination": destination,
            "estimated_time_min": 4,
            "distance_km": 2.1,
            "priority": "High"
        }

    # ========================================================
    # Reset Demo Data
    # ========================================================

    def reset(self):
        """
        Restores default routes.
        """

        self.routes = [
            {
                "id": 1,
                "vehicle": "Response Unit 1",
                "origin": "Emergency Station",
                "destination": "Zone A",
                "distance_km": 1.8,
                "estimated_time_min": 3,
                "status": "available",
                "created_at": datetime.now().isoformat()
            }
        ]

        return True