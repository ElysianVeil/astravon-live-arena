"""
============================================================
Astravon Live Arena
Analytics Reports

Purpose:
    Generates AI analytics reports for crowd monitoring,
    risk assessment and event statistics.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


# ============================================================
# Directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_DIRECTORY = BASE_DIR / "outputs" / "reports"

REPORT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Report Generator
# ============================================================

class ReportGenerator:
    """
    Generates AI Engine reports.
    """

    def __init__(self) -> None:

        self.generated_reports: List[Dict[str, Any]] = []

    # ========================================================
    # Generate Report
    # ========================================================

    def generate(
        self,
        statistics: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        event_name: str = "Astravon Live Arena Event"
    ) -> Dict[str, Any]:
        """
        Creates a report object.
        """

        report = {
            "event_name": event_name,
            "generated_at": datetime.utcnow().isoformat(),
            "statistics": statistics,
            "alerts": alerts,
            "total_alerts": len(alerts)
        }

        self.generated_reports.append(report)

        return report

    # ========================================================
    # Save Report
    # ========================================================

    def save_json(
        self,
        report: Dict[str, Any],
        filename: str | None = None
    ) -> Path:
        """
        Saves a report as JSON.
        """

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = f"report_{timestamp}.json"

        filepath = REPORT_DIRECTORY / filename

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return filepath

    # ========================================================
    # Latest Report
    # ========================================================

    def latest(self) -> Dict[str, Any] | None:
        """
        Returns the most recent report.
        """

        if not self.generated_reports:
            return None

        return self.generated_reports[-1]

    # ========================================================
    # Report History
    # ========================================================

    def history(self) -> List[Dict[str, Any]]:
        """
        Returns all generated reports.
        """

        return self.generated_reports

    # ========================================================
    # Summary
    # ========================================================

    def summary(self) -> Dict[str, Any]:
        """
        Returns reporting statistics.
        """

        return {
            "reports_generated": len(self.generated_reports),
            "latest_report": (
                self.generated_reports[-1]["generated_at"]
                if self.generated_reports
                else None
            )
        }

    # ========================================================
    # Export
    # ========================================================

    def export_all(self) -> List[str]:
        """
        Saves every report to disk.
        """

        exported_files = []

        for index, report in enumerate(
            self.generated_reports,
            start=1
        ):

            filename = f"report_{index}.json"

            path = self.save_json(
                report,
                filename
            )

            exported_files.append(str(path))

        return exported_files

    # ========================================================
    # Reset
    # ========================================================

    def clear(self) -> None:
        """
        Removes all in-memory reports.
        """

        self.generated_reports.clear()


# ============================================================
# Global Instance
# ============================================================

report_generator = ReportGenerator()


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    statistics = {
        "people_count": 286,
        "density": "High",
        "occupancy": 72.4,
        "temperature": 31.6,
        "humidity": 63.1,
        "risk_score": 67
    }

    alerts = [
        {
            "title": "Crowd Density",
            "severity": "Medium"
        },
        {
            "title": "Heat Warning",
            "severity": "High"
        }
    ]

    report = report_generator.generate(
        statistics,
        alerts,
        event_name="University Football Match"
    )

    path = report_generator.save_json(report)

    print(f"Saved: {path}")

    print(report_generator.summary())