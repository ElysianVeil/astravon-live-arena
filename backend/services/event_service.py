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

    def __init__(
        self,
        notification_service=None,
        archive_storage=None,
        statistics_manager=None
    ):

        self.notification_service = notification_service
        self.archive_storage = archive_storage
        self.statistics_manager = statistics_manager

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
        # Runtime State
        # ========================================================

        self.current_event = self.events[0]

        self.event_history = []

        self.total_events_created = len(self.events)

    # ========================================================
    # Runtime
    # ========================================================

    def get_current_event(self):

        return self.current_event


    def get_event_history(self):

        return self.event_history


    def get_total_events_created(self):

        return self.total_events_created

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
    
    def get_events_by_status(

        self,

        status: str

    ):

        return [

            event

            for event in self.events

            if event["status"] == status

        ]
    
    def get_events_by_venue(

        self,

        venue: str

    ):

        return [

            event

            for event in self.events

            if event["venue"] == venue

        ]

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

        self.total_events_created += 1

        self.event_history.append({

            "action": "created",

            "event_id": event["id"],

            "timestamp": datetime.utcnow().isoformat()

        })

        if self.notification_service:

            self.notification_service.broadcast_event(event)

        if self.archive_storage:

            self.archive_storage.archive_event(event)

        self.logger.info(
            f"Event created: {event['name']}"
        )

        self.logger.info(

            f"Creating event "

            f"{request.name} "

            f"({request.venue}) "

            f"capacity={request.capacity}"

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

        if not validate_capacity(request.capacity):

            raise ValueError("Invalid capacity")

        event = self.get_event(event_id)

        if event is None:

            return None

        event["name"] = request.name
        event["venue"] = request.venue
        event["mode"] = request.mode
        event["capacity"] = request.capacity
        event["updated_at"] = datetime.utcnow().isoformat()

        if self.notification_service:

            self.notification_service.broadcast_event(event)

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

            event["deleted_at"] = datetime.utcnow().isoformat()

            if self.archive_storage:

                self.archive_storage.delete_archive(event)

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

            event["status"] = STATUS_COMPLETED
            event["ended_at"] = datetime.utcnow().isoformat()

        event = self.get_event(event_id)

        if event is None:

            return None

        event["status"] = STATUS_ACTIVE
        event["started_at"] = datetime.utcnow().isoformat()

        self.current_event = event
        if self.notification_service:

            self.notification_service.broadcast_event(event)

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

        event["status"] = STATUS_COMPLETED

        event["ended_at"] = datetime.utcnow().isoformat()

        self.current_event = {}

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

            if event["status"] == STATUS_ACTIVE:
                active += 1

            elif event["status"] == STATUS_SCHEDULED:
                scheduled += 1

            elif event["status"] == STATUS_COMPLETED:
                completed += 1

        return {
            "total_events": len(self.events),
            "active_events": active,
            "scheduled_events": scheduled,
            "completed_events": completed
        }
    
    def dashboard(self):

        return {

            "current_event": self.current_event,

            "statistics": self.get_statistics(),

            "total_events_created": self.total_events_created,

            "active_events": self.get_events_by_status(

                STATUS_ACTIVE

            )

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

        self.current_event = self.events[0]

        self.event_history.clear()

        self.total_events_created = 1

        return True
    
# Future:
#
# - TicketService
# - CameraService
# - ZoneService
# - CrowdSimulationService
# - WeatherService
# - AIService