"""
============================================================
Astravon Live Arena
AI Output Manager

Purpose:
    Centralizes all AI Engine outputs before they are
    transmitted to the backend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Any, Dict
import asyncio

from api.http_client import HTTPClient
from api.schemas import StatisticsRequest
from api.websocket_client import WebSocketClient


class OutputManager:
    """
    Sends AI results to the backend.
    """

    def __init__(self) -> None:

        self.http = HTTPClient()

        self.websocket = WebSocketClient()

    # ========================================================
    # Statistics
    # ========================================================

    def send_statistics(
        self,
        statistics: StatisticsRequest
    ) -> bool:
        """
        Sends crowd statistics.
        """
        
        asyncio.run(
            self.websocket.send_statistics(
                statistics
            )
        )

        return self.http.send_statistics(
            statistics
        )

    # ========================================================
    # Detection
    # ========================================================

    def send_detection(
        self,
        detection: Dict[str, Any]
    ) -> bool:
        """
        Sends AI detection results.
        """
        asyncio.run(
            self.websocket.send_detection(
                detection
            )
        )

        return self.http.send_detection(
            detection
        )

    # ========================================================
    # Alert
    # ========================================================

    def send_alert(
        self,
        alert: Dict[str, Any]
    ) -> bool:
        """
        Sends emergency alerts.
        """
        asyncio.run(
            self.websocket.send_alert(
                alert
            )
        )

        return self.http.send_alert(
            alert
        )

    # ========================================================
    # Route
    # ========================================================

    def send_route(
        self,
        route: Dict[str, Any]
    ) -> bool:
        """
        Sends emergency routing information.
        """
        asyncio.run(
            self.websocket.send_route(
                route
            )
        )

        return self.http.calculate_route(
            route
        )

    # ========================================================
    # Report
    # ========================================================

    def send_report(
        self,
        report: Dict[str, Any]
    ) -> bool:
        """
        Sends generated reports.
        """

        return self.http.generate_report(
            report
        )

    # ========================================================
    # Generic
    # ========================================================

    def send(
        self,
        endpoint: str,
        payload: Dict[str, Any]
    ) -> bool:
        """
        Sends custom payloads.
        """

        return self.http._request(
            "POST",
            endpoint,
            payload
        )


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    output = OutputManager()

    output.send_statistics(
        {
            "people_count": 245,
            "density": "Medium",
            "occupancy": 49,
            "temperature": 31.4,
            "risk_score": 42
        }
    )