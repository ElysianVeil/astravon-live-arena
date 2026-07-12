"""
============================================================
Astravon Live Arena
Report Service

Purpose:
    Handles report generation and management.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import List, Optional, Dict

from backend.utils.logger import get_logger
from backend.schemas.report import ReportRequest

from backend.utils.helpers import (
    generate_report_filename
)


class ReportService:
    """
    Business logic for report generation.
    """

    logger = get_logger(
        "ReportService"
    )

    def __init__(self):

        self.reports: List[dict] = []

    # ========================================================
    # Generate Report
    # ========================================================

    def generate_report(
        self,
        request: ReportRequest
    ) -> Dict:
        """
        Generates a report.
        """

        self.logger.info(
            "Generating report"
        )

        report = {
            "id": len(self.reports) + 1,
            "title": request.title,
            "report_type": request.report_type,
            "event": request.event,
            "generated_by": request.generated_by,
            "generated_at": datetime.now().isoformat(),
            "file_name": generate_report_filename(
                request.report_type
            ),
            "status": "Completed",
            "summary": request.summary,
            "data": request.data
        }

        self.reports.append(report)

        self.logger.info(
            "Report generated successfully"
        )

        return report

    # ========================================================
    # Get Reports
    # ========================================================

    def get_reports(self) -> List[Dict]:
        """
        Returns all reports.
        """

        return self.reports

    # ========================================================
    # Get Report
    # ========================================================

    def get_report(
        self,
        report_id: int
    ) -> Optional[Dict]:
        """
        Returns a report by ID.
        """

        for report in self.reports:

            if report["id"] == report_id:

                return report

        return None

    # ========================================================
    # Latest Report
    # ========================================================

    def latest_report(self) -> Optional[Dict]:
        """
        Returns the latest report.
        """

        if not self.reports:

            return None

        return self.reports[-1]

    # ========================================================
    # Delete Report
    # ========================================================

    def delete_report(
        self,
        report_id: int
    ) -> bool:
        """
        Deletes a report.
        """

        report = self.get_report(report_id)

        if report:

            self.reports.remove(report)

            return True

        return False

    # ========================================================
    # Export Report
    # ========================================================

    def download_report(
        self,
        report_id: int
    ) -> Optional[Dict]:
        """
        Simulates downloading a report.
        """

        report = self.get_report(report_id)

        if report is None:

            return None

        return {
            "report_id": report_id,
            "file_name": f"report_{report_id}.json",
            "download_ready": True
        }

    # ========================================================
    # Export All Reports
    # ========================================================

    def export_reports(self) -> Dict:
        """
        Simulates exporting all reports.
        """

        return {
            "total_reports": len(self.reports),
            "status": "Export Complete",
            "exported_at": datetime.now().isoformat()
        }

    # ========================================================
    # Summary
    # ========================================================

    def summary(self) -> Dict:
        """
        Returns report statistics.
        """

        completed = len(self.reports)

        return {
            "total_reports": completed,
            "completed_reports": completed,
            "pending_reports": 0,
            "generated_today": completed
        }

    # ========================================================
    # Search Reports
    # ========================================================

    def search_reports(
        self,
        keyword: str
    ) -> List[Dict]:
        """
        Searches reports by title.
        """

        keyword = keyword.lower()

        return [

            report

            for report in self.reports

            if keyword in report["title"].lower()

        ]

    # ========================================================
    # Report Statistics
    # ========================================================

    def report_statistics(self) -> Dict:
        """
        Returns report metrics.
        """

        report_types = {}

        for report in self.reports:

            report_type = report["report_type"]

            report_types[report_type] = (
                report_types.get(report_type, 0) + 1
            )

        return {
            "total_reports": len(self.reports),
            "report_types": report_types
        }

    # ========================================================
    # Reset Demo Data
    # ========================================================

    def reset(self):
        """
        Clears all reports.
        """

        self.reports.clear()

        return True