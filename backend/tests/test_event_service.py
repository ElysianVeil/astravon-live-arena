"""
============================================================
Event Service Tests
============================================================
"""

from backend.services.event_service import EventService



def test_event_service_creation():

    service = EventService()


    assert service is not None



def test_current_event():

    service = EventService()


    event = service.get_current_event()


    assert event is not None