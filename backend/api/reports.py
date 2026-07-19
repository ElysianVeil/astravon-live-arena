"""
============================================================
Astravon Live Arena
Reports API

Purpose:
    Handles report generation and retrieval.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.report import (
    ReportRequest,
    ReportResponse,
    ReportListResponse
)

from backend.dependencies.services import report_service

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"]
)

# ============================================================
# Services
# ============================================================

# report_service = ReportService()

# ============================================================
# Get Reports
# ============================================================

@router.get(
    "/",
    response_model=ReportListResponse,
    summary="Get Reports"
)
async def get_reports():
    """
    Returns all generated reports.
    """

    reports = report_service.get_reports()

    return ReportListResponse(
        success=True,
        message="Reports retrieved successfully.",
        data=reports
    )

# ============================================================
# Search Reports
# ============================================================

@router.get(
    "/search",
    response_model=ReportListResponse,
    summary="Search Reports"
)
async def search_reports(
    keyword: str
):
    """
    Search reports by title,
    event or report type.
    """

    reports = report_service.search_reports(
        keyword
    )

    return ReportListResponse(
        success=True,
        message="Search completed.",
        data=reports
    )

# ============================================================
# Reports by Type
# ============================================================

@router.get(
    "/type/{report_type}",
    response_model=ReportListResponse,
    summary="Reports By Type"
)
async def reports_by_type(
    report_type: str
):

    reports = report_service.get_reports_by_type(
        report_type
    )

    return ReportListResponse(
        success=True,
        message="Reports retrieved.",
        data=reports
    )

# ============================================================
# Reports by Event
# ============================================================

@router.get(
    "/event/{event}",
    response_model=ReportListResponse,
    summary="Reports By Event"
)
async def reports_by_event(
    event: str
):

    reports = report_service.get_reports_by_event(
        event
    )

    return ReportListResponse(
        success=True,
        message="Reports retrieved.",
        data=reports
    )

# ============================================================
# Reports By Author
# ============================================================

@router.get(
    "/author/{author}",
    response_model=ReportListResponse,
    summary="Reports By Author"
)
async def reports_by_author(
    author: str
):

    reports = report_service.get_reports_by_author(
        author
    )

    return ReportListResponse(
        success=True,
        message="Reports retrieved.",
        data=reports
    )


# ============================================================
# Get Report
# ============================================================

@router.get(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Get Report"
)
async def get_report(
    report_id: int
):
    """
    Returns a single report.
    """

    report = report_service.get_report(report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found."
        )

    return ReportResponse(
        success=True,
        message="Report retrieved successfully.",
        data=report
    )


# ============================================================
# Generate Report
# ============================================================

@router.post(
    "/generate",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Report"
)
async def generate_report(
    request: ReportRequest
):
    """
    Generates a new report.
    """

    report = report_service.generate_report(request)

    return ReportResponse(
        success=True,
        message="Report generated successfully.",
        data=report
    )


# ============================================================
# Download Report
# ============================================================

@router.get(
    "/{report_id}/download",
    summary="Download Report"
)
async def download_report(
    report_id: int
):
    """
    Returns download information
    for a generated report.
    """

    download = report_service.download_report(report_id)

    if download is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return {
        "success": True,
        "message": "Download ready.",
        "data": download
    }


# ============================================================
# Latest Report
# ============================================================

@router.get(
    "/latest",
    response_model=ReportResponse,
    summary="Latest Report"
)
async def latest_report():
    """
    Returns the most recently
    generated report.
    """

    report = report_service.latest_report()

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reports available."
        )

    return ReportResponse(
        success=True,
        message="Latest report retrieved.",
        data=report
    )


# ============================================================
# Current Report
# ============================================================

@router.get(
    "/current",
    response_model=ReportResponse,
    summary="Current Report"
)
async def current_report():

    report = report_service.get_current_report()

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="No active report."
        )

    return ReportResponse(
        success=True,
        message="Current report retrieved.",
        data=report
    )

# ============================================================
# Report History
# ============================================================

@router.get(
    "/history",
    summary="Report History"
)
async def report_history():

    return {

        "success": True,

        "message": "History retrieved.",

        "data": report_service.get_report_history()

    }


# ============================================================
# Dashboard
# ============================================================

@router.get(
    "/dashboard",
    summary="Reports Dashboard"
)
async def dashboard():

    return {

        "success": True,

        "message": "Dashboard loaded.",

        "data": report_service.dashboard()

    }


# ============================================================
# Report Statistics
# ============================================================

@router.get(
    "/statistics",
    summary="Report Statistics"
)
async def statistics():

    return {

        "success": True,

        "message": "Statistics retrieved.",

        "data": report_service.report_statistics()

    }

# ============================================================
# Total Generated
# ============================================================

@router.get(
    "/generated",
    summary="Total Reports Generated"
)
async def total_generated():

    return {

        "success": True,

        "message": "Total reports generated.",

        "data": {

            "total":

            report_service.get_total_generated()

        }

    }

# ============================================================
# Reset
# ============================================================

@router.post(
    "/reset",
    summary="Reset Reports"
)
async def reset():

    report_service.reset()

    return {

        "success": True,

        "message": "Reports reset.",

        "data": {}

    }

# ============================================================
# Report Summary
# ============================================================

@router.get(
    "/summary",
    summary="Report Summary"
)
async def report_summary():
    """
    Returns report statistics.
    """

    summary = report_service.summary()

    return {
        "success": True,
        "message": "Report summary retrieved.",
        "data": summary
    }


# ============================================================
# Delete Report
# ============================================================

@router.delete(
    "/{report_id}",
    summary="Delete Report"
)
async def delete_report(
    report_id: int
):
    """
    Deletes a report.
    """
    
    report = report_service.get_report(report_id)

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    report_service.delete_report(report_id)

    return {
        "success": True,
        "message": "Report deleted successfully.",
        "data": {}
    }


# ============================================================
# Export Reports
# ============================================================

@router.post(
    "/export",
    summary="Export Reports"
)
async def export_reports():
    """
    Exports all reports.
    """

    exported = report_service.export_reports()

    return {
        "success": True,
        "message": "Reports exported successfully.",
        "data": exported
    }