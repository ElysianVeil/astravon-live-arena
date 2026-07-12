"""
============================================================
Statistics Service Tests
============================================================
"""

from backend.services.ai_service import AIService



def test_statistics_generation():

    service = AIService()


    statistics = service.get_statistics()


    assert statistics is not None



def test_current_risk():

    service = AIService()


    risk = service.get_current_risk()


    assert risk is not None