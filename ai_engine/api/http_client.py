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

    def __init__(self):

        self.base_url = (
            settings.BACKEND_URL.rstrip("/")
            + settings.API_PREFIX
        )

        self.timeout = 10

        self.session = requests.Session()

        self.connected = False

        self.total_requests = 0

        self.successful_requests = 0

        self.failed_requests = 0

        self.last_request = None

        self.last_response = None

        self.request_history = []

        self.max_history = 500


    # ========================================================
    # Connection Status
    # ========================================================

    def is_connected(self) -> bool:
        """
        Returns True if backend is reachable.
        """

        response = self.ping()

        self.connected = response is not None

        return self.connected    

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

            self.connected = True

            self.total_requests += 1

            self.successful_requests += 1

            self.last_request = {
                "method": method,
                "endpoint": endpoint,
                "timestamp": datetime.now().isoformat()
            }

            self.last_response = response.status_code

            result = response.json()

            self.request_history.append({

                "endpoint": endpoint,

                "method": method,

                "status": response.status_code,

                "timestamp": datetime.now().isoformat()

            })

            if len(self.request_history) > self.max_history:

                self.request_history.pop(0)

            return result

        except requests.RequestException as error:

            self.connected = False

            self.total_requests += 1

            self.failed_requests += 1

            logger.error(
                f"HTTP Error ({method} {url}): {error}"
            )

            return None
        
    # ========================================================
    # Retry Request
    # ========================================================

    def retry_request(
        self,
        method,
        endpoint,
        data=None,
        retries=3
    ):

        for _ in range(retries):

            result = self._request(
                method,
                endpoint,
                data
            )

            if result is not None:
                return result

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
    # Batch Statistics
    # ========================================================

    def send_statistics_batch(
        self,
        statistics_list
    ):

        return self._request(

            "POST",

            "/statistics/batch",

            {

                "statistics": statistics_list

            }

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
    # Batch Detection
    # ========================================================

    def send_detection_batch(
        self,
        detections
    ):

        return self._request(

            "POST",

            "/ai/detection/batch",

            {

                "detections": detections

            }

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
    # Risk Analysis
    # ========================================================

    def send_risk(
        self,
        risk
    ):

        return self._request(

            "POST",

            "/risk",

            risk

        )

    # ========================================================
    # Heat Data
    # ========================================================

    def send_heat(
        self,
        heat
    ):

        return self._request(

            "POST",

            "/heat",

            heat

        )

    # ========================================================
    # Heat Data
    # ========================================================

    def send_heat(
        self,
        heat
    ):

        return self._request(

            "POST",

            "/heat",

            heat

        )
    
    # ========================================================
    # Prediction
    # ========================================================

    def send_prediction(
        self,
        prediction
    ):

        return self._request(

            "POST",

            "/prediction",

            prediction

        )

    # ========================================================
    # Camera Status
    # ========================================================

    def send_camera_status(
        self,
        status
    ):

        return self._request(

            "POST",

            "/camera/status",

            status

        )

    # ========================================================
    # Engine Status
    # ========================================================

    def send_engine_status(
        self,
        status
    ):

        return self._request(

            "POST",

            "/engine/status",

            status

        )

    # ========================================================
    # Dashboard Snapshot
    # ========================================================

    def send_dashboard(
        self,
        dashboard
    ):

        return self._request(

            "POST",

            "/dashboard",

            dashboard

        )

    # ========================================================
    # Module Information
    # ========================================================

    def info(self):

        return {

            "module": "HTTP Client",

            "status": (

                "Connected"

                if self.connected

                else "Disconnected"

            ),

            "base_url": self.base_url,

            "timeout": self.timeout,

            "total_requests": self.total_requests,

            "successful_requests": self.successful_requests,

            "failed_requests": self.failed_requests,

            "history_size": len(self.request_history)

        }

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):

        success_rate = 0

        if self.total_requests:

            success_rate = round(

                self.successful_requests

                /

                self.total_requests

                *100,

                2

            )

        return {

            "requests": self.total_requests,

            "successful": self.successful_requests,

            "failed": self.failed_requests,

            "success_rate": success_rate,

            "last_request": self.last_request,

            "last_response": self.last_response

        }

    # ========================================================
    # Request History
    # ========================================================

    def history(self):

        return list(self.request_history)

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):

        self.request_history.clear()

        self.total_requests = 0

        self.successful_requests = 0

        self.failed_requests = 0

        self.last_request = None

        self.last_response = None

        self.connected = False

    # ========================================================
    # Dashboard
    # ========================================================

    def dashboard(self):

        return {

            "connected": self.connected,

            "requests": self.total_requests,

            "successful": self.successful_requests,

            "failed": self.failed_requests,

            "success_rate": (

                round(

                    self.successful_requests

                    /

                    self.total_requests

                    *100,

                    2

                )

                if self.total_requests

                else 0

            ),

            "last_request": self.last_request,

            "last_response": self.last_response

        }

    # ========================================================
    # Backend Information
    # ========================================================

    def backend_info(self):

        return self._request(

            "GET",

            "/info"

        )

    # ========================================================
    # Synchronize
    # ========================================================

    def synchronize(
        self,
        payload
    ):

        return self._request(

            "POST",

            "/sync",

            payload

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