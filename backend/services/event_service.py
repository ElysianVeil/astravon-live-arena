"""
============================================================
Astravon Live Arena
Event Service

Purpose:
    Handles event management operations.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import List, Optional

from backend.utils.logger import get_logger


from backend.utils.constants import (
    DEFAULT_EVENT_NAME,
    DEFAULT_VENUE,
    DEFAULT_CAPACITY,
    STATUS_ACTIVE,
    STATUS_SCHEDULED,
    STATUS_COMPLETED
)


from backend.utils.validators import (
    validate_capacity
)

from backend.schemas.event import EventCreateRequest

class EventService:
    """
    Business logic for event management.
    """
    logger = get_logger(
        "EventService"
    )

    def __init__(self):

        self.events: List[dict] = [
            {
                "id": 1,
                "name": DEFAULT_EVENT_NAME,
                "venue": DEFAULT_VENUE,
                "mode": "football",
                "capacity": DEFAULT_CAPACITY,
                "status": STATUS_ACTIVE,
                "created_at": datetime.now().isoformat()
            }
        ]

    # ========================================================
    # Current Event
    # ========================================================

    def get_current_event(self) -> dict:
        """
        Returns the currently active event.
        """

        for event in self.events:

            if event["status"] == "active":

                return event

        return {}

    # ========================================================
    # Event List
    # ========================================================

    def get_events(self) -> List[dict]:
        """
        Returns all events.
        """

        return self.events

    # ========================================================
    # Get Event
    # ========================================================

    def get_event(
        self,
        event_id: int
    ) -> Optional[dict]:
        """
        Returns a specific event.
        """

        for event in self.events:

            if event["id"] == event_id:

                return event

        return None

    # ========================================================
    # Create Event
    # ========================================================

    def create_event(
        self,
        request: EventCreateRequest
    ) -> dict:
        """
        Creates a new event.
        """

        if not validate_capacity(
            request.capacity
        ):

            self.logger.error(
                "Invalid event capacity"
            )

            raise ValueError(
                "Invalid capacity"
            )
        
        self.logger.info(
            "Creating new event"
        )

        event = {
            "id": len(self.events) + 1,
            "name": request.name,
            "venue": request.venue,
            "mode": request.mode,
            "capacity": request.capacity,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }

        self.events.append(event)

        self.logger.info(
            f"Event created: {event['name']}"
        )

        return event

    # ========================================================
    # Update Event
    # ========================================================

    def update_event(
        self,
        event_id: int,
        request
    ) -> Optional[dict]:
        """
        Updates an event.
        """

        event = self.get_event(event_id)

        if event is None:

            return None

        event["name"] = request.name
        event["venue"] = request.venue
        event["mode"] = request.mode
        event["capacity"] = request.capacity

        return event

    # ========================================================
    # Delete Event
    # ========================================================

    def delete_event(
        self,
        event_id: int
    ) -> bool:
        """
        Deletes an event.
        """

        event = self.get_event(event_id)

        if event:

            self.events.remove(event)

            return True

        return False

    # ========================================================
    # Event Status
    # ========================================================

    def start_event(
        self,
        event_id: int
    ) -> Optional[dict]:
        """
        Starts an event.
        """

        for event in self.events:

            event["status"] = "completed"

        event = self.get_event(event_id)

        if event is None:

            return None

        event["status"] = "active"

        return event

    def end_event(
        self,
        event_id: int
    ) -> Optional[dict]:
        """
        Ends an event.
        """

        event = self.get_event(event_id)

        if event is None:

            return None

        event["status"] = "completed"

        return event

    # ========================================================
    # Event Statistics
    # ========================================================

    def get_statistics(self) -> dict:
        """
        Returns event statistics.
        """

        active = 0
        scheduled = 0
        completed = 0

        for event in self.events:

            if event["status"] == "active":
                active += 1

            elif event["status"] == "scheduled":
                scheduled += 1

            elif event["status"] == "completed":
                completed += 1

        return {
            "total_events": len(self.events),
            "active_events": active,
            "scheduled_events": scheduled,
            "completed_events": completed
        }

    # ========================================================
    # Reset Demo Data
    # ========================================================

    def reset(self):
        """
        Restores the default event.
        """

        self.events = [
            {
                "id": 1,
                "name": "Football Match",
                "venue": "Astravon Stadium",
                "mode": "football",
                "capacity": 500,
                "status": "active",
                "created_at": datetime.now().isoformat()
            }
        ]

        return True