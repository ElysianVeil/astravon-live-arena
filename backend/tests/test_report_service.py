"""
============================================================
Report Service Tests
============================================================
"""

from backend.services.report_service import ReportService



def test_report_service_creation():

    service = ReportService()


    assert service is not None



def test_get_reports():

    service = ReportService()


    reports = service.get_reports()


    assert isinstance(
        reports,
        list
    )