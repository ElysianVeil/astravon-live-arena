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

# ============================================================
# Directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIRECTORY = BASE_DIR / "logs"

LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIRECTORY / "analytics.log"

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

    # --------------------------------------------------------
    # Generic Log
    # --------------------------------------------------------

    @staticmethod
    def log(
        event: str,
        data: Dict[str, Any]
    ) -> None:
        """
        Logs a generic analytics event.
        """

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "data": data
        }

        logger.info(
            json.dumps(payload)
        )

    # --------------------------------------------------------
    # Detection
    # --------------------------------------------------------

    @staticmethod
    def log_detection(
        people_count: int,
        confidence: float
    ) -> None:

        AnalyticsLogger.log(
            "detection",
            {
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
            "statistics",
            statistics
        )

    # --------------------------------------------------------
    # Alert
    # --------------------------------------------------------

    @staticmethod
    def log_alert(
        title: str,
        severity: str,
        description: str
    ) -> None:

        AnalyticsLogger.log(
            "alert",
            {
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
            "camera",
            {
                "camera_id": camera_id,
                "status": status
            }
        )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    @staticmethod
    def log_report(
        report_name: str
    ) -> None:

        AnalyticsLogger.log(
            "report",
            {
                "report": report_name
            }
        )

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