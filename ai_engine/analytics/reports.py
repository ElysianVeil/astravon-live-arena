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
import uuid
import gzip
from typing import Any, Dict, List
import hashlib
import csv
from openpyxl import Workbook
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from collections import deque


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

        self.generated_reports = deque(

            maxlen=500

        )        
        self.report_count = 0

        self.total_reports = 0

        self.total_alerts = 0

        self.total_events = set()

        self.last_report_time = None

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

        report_id = str(uuid.uuid4())

        self.report_count += 1

        self.total_reports += 1

        self.total_alerts += len(alerts)

        self.total_events.add(event_name)

        self.last_report_time = datetime.utcnow().isoformat()

        report = {
            "report_version": "2.0",
            "report_id": report_id,
            "report_number": self.report_count,
            "event_name": event_name,

            "generated_at": datetime.utcnow().isoformat(),

            "crowd":{

                "counter":...,

                "density":...,

                "occupancy":...,

                "movement":...,

                "trends":...,

                "congestion":...

            },

            "camera":{

                "camera_id":...,

                "camera_name":...,

                "venue":...,

                "city":...,

                "country":...,

                "coordinates":{

                    "latitude":...,

                    "longitude":...

                }

            },

            "zones":{

                "Entrance":{

                    "people":12

                },

                "VIP":{

                    "people":6

                }

            },

            "alerts":{

                "total":len(alerts),

                "active":alerts

            },

            "risk":{

                "score":...,

                "level":...,

                "recommendation":...,

                "heatstroke_probability":...,

                "stampede_probability":...

            },

            "performance":{

                "fps":...,

                "processing_time":...,

                "uptime":...,

                "frames_processed":...,

                "average_processing_time":...

            },

            "environment":{

                "temperature":31.4,

                "humidity":66,

                "heat_index":35,

                "wind_speed":8,

                "weather":"Sunny"

            },

            "summary":{

                "highest_risk":"High",

                "peak_people":...,

                "average_people":...,

                "total_alerts":...,

                "overall_status":"Operational"

            },

            "engine":{

                "name":"Astravon Live Arena",

                "version":"1.0.0",

                "status":"Running"

            },

            "checksum":...
        }

        checksum = hashlib.sha256(

            json.dumps(
                report,
                sort_keys=True
            ).encode()

        ).hexdigest()

        report["checksum"] = checksum

        self.generated_reports.append(report)

        return report

    # ========================================================
    # Save Report
    # ========================================================

    def save_json(
        self,
        report: Dict[str, Any],
        filename: str | None = None,
        event_name=None
    ) -> Path:
        """
        Saves a report as JSON.
        """

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_name = (
                event_name
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            filename = f"{safe_name}_{timestamp}.json"

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
    
    def save_compressed(
        self,
        report,
        filename=None,
        event_name=None
    ):
        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_name = event_name.replace(" ", "_")

            filename = f"{safe_name}_{timestamp}.json.gz"

        filepath = REPORT_DIRECTORY / filename

        with gzip.open(
            filepath,
            "wt",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return filepath
    
    def save_csv(
        self,
        report: Dict[str, Any],
        filename: str | None = None,
        event_name: str | None = None
    ) -> Path:
        """
        Exports report as CSV.
        """

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_name = (
                event_name or report["event_name"]
            ).replace(" ", "_")

            filename = f"{safe_name}_{timestamp}.csv"

        filepath = REPORT_DIRECTORY / filename

        flattened = {}

        def flatten(prefix, value):

            if isinstance(value, dict):

                for k, v in value.items():

                    flatten(
                        f"{prefix}.{k}" if prefix else k,
                        v
                    )

            elif isinstance(value, list):

                flattened[prefix] = json.dumps(value)

            else:

                flattened[prefix] = value

        flatten("", report)

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(flattened.keys())

            writer.writerow(flattened.values())

        return filepath
    
    def save_csv(
        self,
        report: Dict[str, Any],
        filename: str | None = None,
        event_name: str | None = None
    ) -> Path:
        """
        Exports report as CSV.
        """

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_name = (
                event_name or report["event_name"]
            ).replace(" ", "_")

            filename = f"{safe_name}_{timestamp}.csv"

        filepath = REPORT_DIRECTORY / filename

        flattened = {}

        def flatten(prefix, value):

            if isinstance(value, dict):

                for k, v in value.items():

                    flatten(
                        f"{prefix}.{k}" if prefix else k,
                        v
                    )

            elif isinstance(value, list):

                flattened[prefix] = json.dumps(value)

            else:

                flattened[prefix] = value

        flatten("", report)

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(flattened.keys())

            writer.writerow(flattened.values())

        return filepath
    
    def save_html(
        self,
        report: Dict[str, Any],
        filename: str | None = None,
        event_name: str | None = None
    ) -> Path:
        """
        Exports report as HTML.
        """

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_name = (
                event_name or report["event_name"]
            ).replace(" ", "_")

            filename = f"{safe_name}_{timestamp}.html"

        filepath = REPORT_DIRECTORY / filename

        html = f"""
    <!DOCTYPE html>
    <html>

    <head>

    <meta charset="UTF-8">

    <title>{report['event_name']}</title>

    <style>

    body {{

        font-family: Arial;

        margin:40px;

    }}

    table {{

        border-collapse:collapse;

        width:100%;

    }}

    td,th {{

        border:1px solid #ddd;

        padding:8px;

    }}

    th {{

        background:#222;

        color:white;

    }}

    pre {{

        white-space:pre-wrap;

    }}

    </style>

    </head>

    <body>

    <h1>Astravon Live Arena Report</h1>

    <h2>{report["event_name"]}</h2>

    <table>

    <tr>

    <th>Section</th>

    <th>Content</th>

    </tr>
    """

        for key, value in report.items():

            html += f"""
    <tr>

    <td>{key}</td>

    <td><pre>{json.dumps(value, indent=4)}</pre></td>

    </tr>
    """

        html += """

    </table>

    </body>

    </html>

    """

        filepath.write_text(
            html,
            encoding="utf-8"
        )

        return filepath
    
    def save_pdf(
        self,
        report: Dict[str, Any],
        filename: str | None = None,
        event_name: str | None = None
    ) -> Path:
        """
        Exports report as PDF.
        """

        if filename is None:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_name = (
                event_name or report["event_name"]
            ).replace(" ", "_")

            filename = f"{safe_name}_{timestamp}.pdf"

        filepath = REPORT_DIRECTORY / filename

        document = SimpleDocTemplate(
            str(filepath)
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(

            Paragraph(

                "Astravon Live Arena Report",

                styles["Title"]

            )

        )

        elements.append(

            Spacer(
                1,
                12
            )

        )

        def add_section(
            title,
            value
        ):

            elements.append(

                Paragraph(

                    f"<b>{title}</b>",

                    styles["Heading2"]

                )

            )

            elements.append(

                Paragraph(

                    f"<pre>{json.dumps(value, indent=4)}</pre>",

                    styles["Code"]

                )

            )

            elements.append(

                Spacer(
                    1,
                    12
                )

            )

        for key, value in report.items():

            add_section(
                key,
                value
            )

        document.build(elements)

        return filepath
    
    def info(self):

        return {

            "generator":"Report Generator",

            "reports_generated":self.report_count,

            "reports_in_memory":len(self.generated_reports),

            "export_directory":str(REPORT_DIRECTORY),

            "latest_report":(

                self.latest()["generated_at"]

                if self.latest()

                else None

            )

        }

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
    
    def get_report(
        self,
        report_id
    ):

        for report in self.generated_reports:

            if report["report_id"] == report_id:

                return report

        return None

    def get_reports(
        self,
        event_name=None,
        date=None
    ):

        reports = list(self.generated_reports)

        if event_name:

            reports = [

                r

                for r in reports

                if r["event_name"] == event_name

            ]

        if date:

            reports = [

                r

                for r in reports

                if r["generated_at"].startswith(date)

            ]

        return reports

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

            "reports_generated": self.total_reports,

            "reports_in_memory": len(self.generated_reports),

            "total_alerts": self.total_alerts,

            "total_events": len(self.total_events),

            "latest_report": self.last_report_time,

            "export_directory": str(REPORT_DIRECTORY)

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

        self.report_count = 0

        self.total_reports = 0

        self.total_alerts = 0

        self.total_events.clear()

        self.last_report_time = None


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