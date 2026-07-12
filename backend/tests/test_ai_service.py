"""
============================================================
AI Service Tests
============================================================
"""

from datetime import datetime
from backend.services.ai_service import AIService
from backend.schemas.detection import DetectionRequest



def test_ai_service_initialization():

    service = AIService()


    assert service is not None



def test_detection_processing():

    service = AIService()


    result = service.process_detection(
        DetectionRequest(
            people_count=100,
            detected_objects=100,
            density="Medium",
            occupancy=100,
            temperature=25.0,
            humidity=50.0,
            heat_index=27.0,
            risk_score=50,
            risk_level="Medium",
            confidence=0.95,
            fps=30,
            processing_time=0.02,
            timestamp=datetime.now()
        )
    )


    assert result is not None