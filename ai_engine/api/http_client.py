"""
============================================================
Astravon Live Arena
HTTP Client

Purpose:
    Handles HTTP communication between the AI Engine
    and the FastAPI backend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import logging
from pydantic import BaseModel
from typing import Any, Dict, Optional
from api.schemas import StatisticsRequest
from api.detection import DetectionRequest

import requests

from config import settings
from datetime import datetime
import numpy as np

def to_json(obj):

    if isinstance(obj, dict):
        return {
            k: to_json(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [
            to_json(v)
            for v in obj
        ]

    if isinstance(obj, tuple):
        return tuple(
            to_json(v)
            for v in obj
        )

    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if hasattr(obj, "model_dump"):
        return to_json(obj.model_dump())

    return obj


# ============================================================
# Logger
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# HTTP Client
# ============================================================

class HTTPClient:
    """
    Sends data to the backend REST API.
    """

    def __init__(self) -> None:

        self.base_url = (
            settings.BACKEND_URL.rstrip("/")
            + settings.API_PREFIX
        )

        self.timeout = 10

    

    # ========================================================
    # Internal Request
    # ========================================================

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Performs an HTTP request.
        """

        url = f"{self.base_url}{endpoint}"

        try:
            if data is not None:
                data = to_json(data)

            response = requests.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:

            logger.error(
                f"HTTP Error ({method} {url}): {error}"
            )

            return None

    # ========================================================
    # Health Check
    # ========================================================

    def ping(self) -> Optional[Dict[str, Any]]:
        """
        Checks whether the backend is online.
        """

        return self._request(
            "GET",
            "/status"
        )

    # ========================================================
    # Statistics
    # ========================================================

    def send_statistics(
        self,
        statistics: StatisticsRequest
    ) -> Optional[Dict[str, Any]]:
        """
        Sends crowd statistics.
        """

        return self._request(
            "POST",
            "/statistics/",
            statistics
        )

    # ========================================================
    # Detection
    # ========================================================

    def send_detection(
        self,
        detection: DetectionRequest | dict
    ) -> Optional[Dict[str, Any]]:
        """
        Sends AI detection results.
        """
        if isinstance(detection, BaseModel):
            detection = detection.model_dump(mode="json")

        return self._request(
            "POST",
            "/ai/detection",
            detection
        )

    # ========================================================
    # Alert
    # ========================================================

    def send_alert(
        self,
        alert: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Sends an alert.
        """

        return self._request(
            "POST",
            "/alerts/",
            alert
        )

    # ========================================================
    # Report
    # ========================================================

    def generate_report(
        self,
        report: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Requests report generation.
        """

        return self._request(
            "POST",
            "/reports/generate",
            report
        )

    # ========================================================
    # Route
    # ========================================================

    def calculate_route(
        self,
        route: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Requests an emergency route.
        """

        return self._request(
            "POST",
            "/routes/",
            route
        )


# ============================================================
# Global Client
# ============================================================

http_client = HTTPClient()


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    print(http_client.ping())

    statistics = {
        "people_count": 148,
        "density": "Medium",
        "occupancy": 61.5,
        "movement": "Normal",
        "congestion": "Low",
        "temperature": 30.8,
        "humidity": 67.2,
        "heat_index": 33.1,
        "risk_score": 42
    }

    print(http_client.send_statistics(statistics))