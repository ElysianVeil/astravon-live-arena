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
import cv2
import base64
import threading

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

        self.loop = asyncio.new_event_loop()

        self.thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )

        self.thread.start()

        asyncio.run_coroutine_threadsafe(
            self.websocket.connect(),
            self.loop
        ).result()

    # =====================================================
    # Background Event Loop
    # =====================================================

    def _run_loop(self):

        asyncio.set_event_loop(self.loop)

        self.loop.run_forever()

    # =====================================================
    # Helper
    # =====================================================

    def _submit(self, coroutine):

        if self.loop.is_closed():
            return

        return asyncio.run_coroutine_threadsafe(
            coroutine,
            self.loop
        )


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
        
        self._submit(
            self.websocket.send_statistics(
                statistics
            )
        )

        # future.result(timeout=2)

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
        self._submit(
            self.websocket.send_detection(
                detection
            )
        )

        # future.result(timeout=2)

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
        self._submit(
            self.websocket.send_alert(
                alert
            )
        )

        # future.result(timeout=2)

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
        self._submit(
            self.websocket.send_route(
                route
            )
        )

        # future.result(timeout=2)

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
    # Camera Frame
    # ========================================================

    def send_camera_frame(
        self,
        payload
    ) -> bool:
        """
        Sends an annotated camera frame.
        """
        # Copy so we don't modify the caller's dictionary
        camera_payload = payload.copy()

        frame = camera_payload.pop("frame")

        success, buffer = cv2.imencode(".jpg", frame)

        if not success:
            return False

        camera_payload["frame"] = base64.b64encode(buffer).decode("utf-8")

        print(f"Sending frame ({camera_payload['width']}x{camera_payload['height']})")

        self._submit(
            self.websocket.send_camera_frame(
                camera_payload
            )
        )

        return True

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
    
    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(self):
        if self.loop.is_closed():
            return

        if self.websocket.connected:
            future = asyncio.run_coroutine_threadsafe(

                self.websocket.disconnect(),

                self.loop

            )

            try:

                future.result(timeout=5)

            except Exception as error:

                print(error)

        self.loop.call_soon_threadsafe(

            self.loop.stop

        )

        self.thread.join(timeout=5)

        self.loop.close()


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