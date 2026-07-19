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

    def __init__(
        self,
        ai_service=None,
        statistics_manager=None,
        event_service=None,
        archive_storage=None,
        notification_service=None
    ):

        self.ai_service = ai_service
        self.statistics_manager = statistics_manager
        self.event_service = event_service
        self.archive_storage = archive_storage
        self.notification_service = notification_service

        self.reports = []

        self.report_history = []

        self.total_reports_generated = 0

        self.current_report = None

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
        started = datetime.utcnow()

        report_data = request.data

        if report_data is None:

            report_data = {

                "statistics": (

                    self.statistics_manager.dashboard()

                    if self.statistics_manager

                    else {}

                ),

                "event": (

                    self.event_service.get_current_event()

                    if self.event_service

                    else {}

                ),

                "engine": (

                    self.ai_service.get_engine()

                    if self.ai_service

                    else {}

                )

            }

        finished = datetime.utcnow()
        generation_time = (
            finished-started
        ).total_seconds()*1000

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
            "data": report_data,
            "updated_at": datetime.utcnow().isoformat(),
            "generation_time_ms": generation_time
            
        }

        

        self.current_report = report

        self.total_reports_generated += 1

        self.reports.append(report)

        if self.archive_storage:

            self.archive_storage.archive_report(

                report

            )

        if self.notification_service:

            self.notification_service.broadcast_report(

                report

            )

        self.logger.info(

            f"Generating "

            f"{request.report_type} "

            f"report "

            f"for "

            f"{request.event}"

        )

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
            if self.archive_storage:

                self.archive_storage.archive_deleted_report(

                    report

                )

            self.report_history.append({

                "report_id": report["id"],

                "action":"deleted",

                "timestamp": datetime.utcnow().isoformat()

            })

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

            "report": report,

            "download_ready": True,

            "file_name": report["file_name"],

            "generated_at": report["generated_at"]

        }

    # ========================================================
    # Export All Reports
    # ========================================================

    def export_reports(self) -> Dict:
        """
        Simulates exporting all reports.
        """

        return {

            "status":"Export Complete",

            "exported_at": datetime.utcnow().isoformat(),

            "total_reports": len(self.reports),

            "reports": self.reports

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

            if (

                keyword in report["title"].lower()

                or

                keyword in report["event"].lower()

                or

                keyword in report["report_type"].lower()

            )

        ]

    def get_reports_by_type(

        self,

        report_type: str

    ):

        return [

            report

            for report in self.reports

            if report["report_type"] == report_type

        ]

    def get_reports_by_event(

        self,

        event: str

    ):

        return [

            report

            for report in self.reports

            if report["event"] == event

        ]
    
    def get_reports_by_author(

        self,

        author: str

    ):

        return [

            report

            for report in self.reports

            if report["generated_by"] == author

        ]
    
    def get_current_report(self):

      return self.current_report
    
    def get_report_history(self):

        return self.report_history
    
    def get_total_generated(self):

        return self.total_reports_generated
    
    def dashboard(self):

        return {

            "current_report": self.current_report,

            "statistics": self.summary(),

            "latest_report": self.latest_report(),

            "total_generated":

                self.total_reports_generated

        }
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

        self.report_history.clear()

        self.current_report = None

        self.total_reports_generated = 0

        return True