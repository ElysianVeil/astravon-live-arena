"""
============================================================
Astravon Live Arena
Analytics Logger

Purpose:
    Logs AI analytics, detections, alerts,
    reports and system events.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
import uuid
from collections import deque

# ============================================================
# Directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIRECTORY = BASE_DIR / "logs"

LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIRECTORY / (
    f"analytics_{datetime.now():%Y%m%d}.log"
)

# ============================================================
# Logger Configuration
# ============================================================

logger = logging.getLogger("analytics")

logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

# ============================================================
# Analytics Logger
# ============================================================

class AnalyticsLogger:
    """
    Handles AI analytics logging.
    """
    def __init__(self) -> None:
        self.history = deque(maxlen=1000)

        self.events_logged = 0
        self.alerts_logged = 0
        self.total_detections = 0
        self.reports_logged = 0
        self.errors_logged = 0

        self.session_id = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S"
        )

    # --------------------------------------------------------
    # Generic Log
    # --------------------------------------------------------

    @staticmethod
    def log(
        self,
        event: str,
        data: Dict[str, Any],
        component=None
    ) -> None:
        """
        Logs a generic analytics event.
        """

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "session": self.session_id,
            "event_id": str(uuid.uuid4()),
            "component": component,
            "event": event,
            "engine":{

                "status":"Running",

                "version":"1.0.0"

            },
            "data": data
        }

        self.history.append(payload)

        self.events_logged += 1

        logger.info(
            json.dumps(payload)
        )

    # --------------------------------------------------------
    # Detection
    # --------------------------------------------------------

    @staticmethod
    def log_detection(
        self,
        people_count: int,
        confidence: float
    ) -> None:
        self.total_detections += people_count

        AnalyticsLogger.log(
            component="Detector",
            event="detection",
            data={
                "people_count": people_count,
                "confidence": confidence
            }
        )

    # --------------------------------------------------------
    # Crowd Statistics
    # --------------------------------------------------------

    @staticmethod
    def log_statistics(
        statistics: Dict[str, Any]
    ) -> None:

        AnalyticsLogger.log(
            component="Crowd Statistics",
            event="statistics",
            data=statistics
        )

    # --------------------------------------------------------
    # Alert
    # --------------------------------------------------------

    @staticmethod
    def log_alert(
        self,
        title: str,
        severity: str,
        description: str
    ) -> None:
        self.alerts_logged += 1

        AnalyticsLogger.log(
            component="Alerts",
            event="alert",
            data={
                "title": title,
                "severity": severity,
                "description": description
            }
        )

    # --------------------------------------------------------
    # Camera
    # --------------------------------------------------------

    @staticmethod
    def log_camera(
        camera_id: str,
        status: str
    ) -> None:

        AnalyticsLogger.log(
            component="Camera",
            event="camera",
            data={
                "camera":{

                    "id": camera_id,

                    "name":...,

                    "venue":...

                },
                "status": status
            }
        )

    def log_performance(
        self,
        metrics
    ):
        AnalyticsLogger.log(
            component="Performance Statistics",
            event="performance",
            data=metrics
        )

    def log_analytics(
        self,
        statistics: Dict[str, Any]
    ) -> None:
        """
        Logs the complete CrowdStatistics object.
        """

        self.log(
            component="Crowd Statistics",
            event="Analytics",
            data=statistics
        )

    def log_risk(
        self,
        risk: Dict[str, Any]
    ) -> None:
        """
        Logs complete risk analysis.
        """

        self.log(
            component="Risk Engine",
            event="Risk Analysis",
            data={
                "risk_score": risk.get("risk_score"),
                "risk_level": risk.get("risk_level"),
                "recommendation": risk.get("recommendation"),
                "heatstroke_probability": risk.get(
                    "heatstroke_probability"
                ),
                "stampede_probability": risk.get(
                    "stampede_probability"
                )
            }
        )

    def log_zone(
        self,
        zone_name: str,
        people: int,
        occupancy: float
    ) -> None:
        """
        Logs zone information.
        """

        self.log(
            component="Zones",
            event="Zone Update",
            data={
                "zone": zone_name,
                "people": people,
                "occupancy": occupancy
            }
        )

    def log_movement(
        self,
        movement: Dict[str, Any]
    ) -> None:
        """
        Logs movement analytics.
        """

        self.log(
            component="Movement",
            event="Movement Analysis",
            data={
                "average_speed": movement.get("average_speed"),
                "flow_level": movement.get("flow_level"),
                "crowd_direction": movement.get(
                    "crowd_direction"
                ),
                "moving_people": movement.get(
                    "moving_people"
                ),
                "stationary_people": movement.get(
                    "stationary_people"
                )
            }
        )

    def log_environment(
        self,
        weather: Dict[str, Any]
    ) -> None:
        """
        Logs environmental conditions.
        """

        self.log(
            component="Environment",
            event="Weather Update",
            data={
                "temperature": weather.get("temperature"),
                "humidity": weather.get("humidity"),
                "heat_index": weather.get("heat_index"),
                "wind_speed": weather.get("wind_speed"),
                "weather_code": weather.get("weather_code")
            }
        )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    @staticmethod
    def log_report(
        self,
        report: Dict[str, Any]
    ) -> None:
        """
        Logs generated reports.
        """

        self.reports_logged += 1

        self.log(
            component="Reports",
            event="Report Generated",
            data={
                "report_id": report.get("report_id"),
                "event_name": report.get("event_name"),
                "generated_at": report.get("generated_at"),
                "checksum": report.get("checksum")
            }
        )
    
    def search(
        self,
        event: str | None = None,
        component: str | None = None
    ):
        """
        Searches the in-memory log history.
        """

        results = []

        for record in self.history:

            if event:

                if record.get("event") != event:
                    continue

            if component:

                if record.get("component") != component:
                    continue

            results.append(record)

        return results

    def summary(self):
        """
        Returns logger summary.
        """

        latest = None

        if self.history:
            latest = self.history[-1]

        return {

            "session": self.session_id,

            "events": self.events_logged,

            "alerts": self.alerts_logged,

            "errors": self.errors_logged,

            "reports": self.reports_logged,

            "detections": self.total_detections,

            "latest": latest

        }
    
    def info(self):
        """
        Returns logger information.
        """

        return {

            "logger": "Analytics Logger",

            "status": "Running",

            "session": self.session_id,

            "log_directory": str(LOG_DIRECTORY),

            "log_file": str(LOG_FILE),

            "events_logged": self.events_logged,

            "reports_logged": self.reports_logged,

            "alerts_logged": self.alerts_logged,

            "errors_logged": self.errors_logged,

            "history_size": len(self.history)

        }

    # --------------------------------------------------------
    # Error
    # --------------------------------------------------------

    @staticmethod
    def log_error(
        error: Exception
    ) -> None:

        logger.error(str(error))

    # --------------------------------------------------------
    # Information
    # --------------------------------------------------------

    @staticmethod
    def info(
        message: str
    ) -> None:

        logger.info(message)

    # --------------------------------------------------------
    # Warning
    # --------------------------------------------------------

    @staticmethod
    def warning(
        message: str
    ) -> None:

        logger.warning(message)

    @staticmethod
    def debug(message):
        logger.debug(message)

    @staticmethod
    def critical(message):
        logger.critical(message)


# ============================================================
# Global Instance
# ============================================================

analytics_logger = AnalyticsLogger()


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    analytics_logger.log_detection(
        people_count=128,
        confidence=0.96
    )

    analytics_logger.log_statistics(
        {
            "density": "Medium",
            "temperature": 31.5,
            "risk_score": 47
        }
    )

    analytics_logger.log_alert(
        title="Crowd Density",
        severity="Medium",
        description="Density threshold exceeded."
    )

    analytics_logger.log_camera(
        camera_id="Camera-01",
        status="Connected"
    )

    analytics_logger.log_report(
        "event_report.pdf"
    )