"""
============================================================
Astravon Live Arena
Report Schemas

Purpose:
    Pydantic schemas for report generation and
    retrieval.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import List, Optional, Any

from pydantic import Field

from backend.schemas.common import (
    AstravonSchema,
    SuccessResponse
)


# ============================================================
# Report Request
# ============================================================

class ReportRequest(AstravonSchema):
    """
    Request schema for generating reports.
    """

    title: str = Field(
        min_length=3,
        max_length=150
    )

    report_type: str = Field(
        default="Event Summary",
        max_length=50
    )

    event_name: str = Field(
        min_length=2,
        max_length=100
    )

    venue: Optional[str] = None

    generated_by: str = Field(
        default="System",
        max_length=100
    )

    description: Optional[str] = None


# ============================================================
# Report Data
# ============================================================

class ReportData(AstravonSchema):
    """
    Report response payload.
    """

    id: int

    title: str

    report_type: str

    description: Optional[str] = None

    event_name: str

    venue: Optional[str] = None

    summary: Optional[str] = None

    recommendations: Optional[str] = None

    people_count: int

    highest_density: str

    average_temperature: int

    highest_risk_score: int

    total_alerts: int

    report_data: Optional[Any] = None

    file_name: Optional[str] = None

    file_type: str

    generated_by: str

    status: str

    created_at: datetime


# ============================================================
# Report Response
# ============================================================

class ReportResponse(
    SuccessResponse
):
    """
    Single report response.
    """

    data: Optional[ReportData] = None


# ============================================================
# Report List Response
# ============================================================

class ReportListResponse(
    SuccessResponse
):
    """
    Multiple reports response.
    """

    data: List[ReportData] = []


# ============================================================
# Report Summary
# ============================================================

class ReportSummary(AstravonSchema):
    """
    Report dashboard summary.
    """

    total_reports: int

    completed_reports: int

    pending_reports: int

    latest_report: Optional[str] = None


# ============================================================
# Report Summary Response
# ============================================================

class ReportSummaryResponse(
    SuccessResponse
):
    """
    Report summary response.
    """

    data: Optional[ReportSummary] = None


# ============================================================
# Report Export
# ============================================================

class ReportExportResponse(
    SuccessResponse
):
    """
    Report export response.
    """

    data: Optional[dict] = None