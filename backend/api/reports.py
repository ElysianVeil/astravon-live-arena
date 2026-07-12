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

    report = report_service.get_report(report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found."
        )

    download = report_service.download_report(report_id)

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

    deleted = report_service.delete_report(report_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found."
        )

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