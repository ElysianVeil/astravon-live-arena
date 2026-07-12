"""
Astravon Live Arena
Service Dependencies
"""

from backend.services.ai_service import AIService
from backend.services.event_service import EventService
from backend.services.report_service import ReportService
from backend.services.route_service import RouteService


# Single instances shared across API

ai_service = AIService()

event_service = EventService()

report_service = ReportService()

route_service = RouteService()