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

    def __init__(
        self,
        ai_service=None,
        event_service=None,
        notification_service=None,
        archive_storage=None,
        statistics_manager=None
    ):

        self.ai_service = ai_service

        self.event_service = event_service

        self.notification_service = notification_service

        self.archive_storage = archive_storage

        self.statistics_manager = statistics_manager

        self.routes = []

        self.route_history = []

        self.active_dispatches = []

        self.current_route = None

        self.total_routes_created = 0

        self.total_dispatches = 0

        self.available_units = {

            "ambulance": 5,

            "police": 6,

            "fire": 3,

            "security": 8

        }

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

        origin,

        destination,

        priority="Normal"

    ):

        route = {

            "origin": origin,

            "destination": destination,

            "distance_km": 2.4,

            "estimated_time_min": 5,

            "traffic": "Low",

            "priority": priority,

            "status": "Ready",

            "generated_at": datetime.utcnow().isoformat()

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

            "dispatch_time": datetime.utcnow().isoformat()

        }

        self.active_dispatches.append(dispatch)

        self.total_dispatches += 1

        if self.notification_service:

            self.notification_service.broadcast_dispatch(

                dispatch

            )

        return dispatch
    
    # ========================================================
    # Complete Route
    # ========================================================

    def complete_route(

        self,

        route_id

    ):

        route = self.get_route(route_id)

        if route is None:

            return None

        route["status"] = "completed"

        route["completed_at"] = datetime.utcnow().isoformat()

        self.route_history.append({

            "route_id": route_id,

            "action": "completed",

            "timestamp": datetime.utcnow().isoformat()

        })

        if self.archive_storage:

            self.archive_storage.archive_completed_route(

                route

            )

        return route

    def cancel_route(

        self,

        route_id

    ):

        route = self.get_route(route_id)

        if route is None:

            return None

        route["status"] = "cancelled"

        route["cancelled_at"] = datetime.utcnow().isoformat()

        return route

    def get_active_routes(self):

        return [

            route

            for route in self.routes

            if route["status"] in (

                "planned",

                "dispatched",

                "active"

            )

        ]

    def get_route_history(self):

        return self.route_history
    
    def get_current_route(self):

        return self.current_route

    def dispatch_dashboard(self):

        return {

            "active_dispatches":

                len(self.active_dispatches),

            "available_units":

                self.available_units,

            "total_routes":

                len(self.routes),

            "total_dispatches":

                self.total_dispatches

        }

    def vehicle_status(self):

        return self.available_units

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

            "vehicle_status": "available",

            "origin": request.incident_location,

            "destination": request.destination,

            "distance_km": 0,

            "estimated_time_min": 0,

            "traffic_level": "Unknown",

            "priority": "Normal",

            "status": "planned",

            "created_at": datetime.utcnow().isoformat(),

            "updated_at": datetime.utcnow().isoformat()

        }

        self.routes.append(
            route
        )

        self.current_route = route

        self.total_routes_created += 1

        self.route_history.append({

            "route_id": route["id"],

            "action": "created",

            "timestamp": datetime.utcnow().isoformat()

        })

        if self.archive_storage:

            self.archive_storage.archive_route(route)

        if self.notification_service:

            self.notification_service.broadcast_route(route)

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

            "total_routes":

                len(self.routes),

            "active_routes":

                len(

                    self.get_active_routes()

                ),

            "dispatches":

                self.total_dispatches,

            "available_units":

                self.available_units

        }

    def dashboard(self):

        return {

            "statistics":

                self.get_statistics(),

            "current_route":

                self.current_route,

            "dispatches":

                self.active_dispatches,

            "history":

                len(self.route_history)

        }

    def search_routes(

        self,

        keyword

    ):

        keyword = keyword.lower()

        return [

            route

            for route in self.routes

            if (

                keyword in route["origin"].lower()

                or

                keyword in route["destination"].lower()

                or

                keyword in route["vehicle"].lower()

            )

        ]

    # ========================================================
    # Recommended Route
    # ========================================================

    def recommended_route(

        self,

        destination

    ):

        current_event = {}

        if self.event_service:

            current_event = self.event_service.get_current_event()

        return {

            "vehicle": "Response Unit 1",

            "destination": destination,

            "estimated_time_min": 4,

            "distance_km": 2.1,

            "priority": "High",

            "event": current_event

        }

    # ========================================================
    # Reset Demo Data
    # ========================================================

    def reset(self):
        """
        Restores default routes.
        """

        self.routes.clear()

        self.route_history.clear()

        self.active_dispatches.clear()

        self.current_route = None

        self.total_routes_created = 0

        self.total_dispatches = 0

        self.available_units = {

            "ambulance": 5,

            "police": 6,

            "fire": 3,

            "security": 8

        }

        return True

    