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
from datetime import datetime
from api.schemas import StatisticsRequest
from api.websocket_client import WebSocketClient


class OutputManager:
    """
    Sends AI results to the backend.
    """

    def __init__(self) -> None:

        self.http = HTTPClient()
        self.websocket = WebSocketClient()

        # Transmission statistics
        self.messages_sent = 0
        self.messages_failed = 0
        self.websocket_messages = 0
        self.http_messages = 0

        # Queue statistics
        self.total_frames_sent = 0
        self.total_statistics_sent = 0
        self.total_alerts_sent = 0
        self.total_detections_sent = 0
        self.total_reports_sent = 0

        # Health
        self.started_at = datetime.now()
        self.last_transmission = None
        self.last_error = None

        # Cache
        self.last_statistics = None
        self.last_detection = None
        self.last_alert = None
        self.last_route = None
        self.last_report = None

        # History
        from collections import deque
        self.history = deque(maxlen=500)

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
    
    # =====================================================
    # Log Transmission
    # =====================================================

    def _log(
        self,
        message_type: str,
        success: bool,
        payload: dict | None = None
    ):

        entry = {

            "timestamp": datetime.now().isoformat(),

            "type": message_type,

            "success": success,

            "payload": payload

        }

        self.history.append(entry)

        self.last_transmission = entry

        if success:
            self.messages_sent += 1
        else:
            self.messages_failed += 1


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
        
        # self._submit(
        #     self.websocket.send_statistics(
        #         statistics
        #     )
        # )

        # future.result(timeout=2)

        self.last_statistics = statistics

        self.total_statistics_sent += 1

        ws_success = True

        future = self._submit(
            self.websocket.send_statistics(statistics)
        )

        if future:
            try:
                future.result(timeout=2)
                self.websocket_messages += 1
            except Exception:
                ws_success = False

        http_success = self.http.send_statistics(statistics)

        if http_success:
            self.http_messages += 1

        success = ws_success or bool(http_success)

        self._log(
            "statistics",
            success,
            statistics
        )

        return success

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

        self.last_detection = detection

        self.total_detections_sent += 1

        # future.result(timeout=2)

        http_success = self.http.send_detection(
            detection
        )
        
        self._log(
            "detection",
            True,
            detection
        )

        return http_success

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

        self.last_alert = alert

        self.total_alerts_sent += 1

        # future.result(timeout=2)

        alert_success = self.http.send_alert(
            alert
        )
    
        self._log(
            "alert",
            True,
            alert
        )

        return alert_success

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

        self.last_route = route

        # future.result(timeout=2)

        route_success = self.http.calculate_route(
            route
        )

        self._log(
            "route",
            True,
            route
        )

        return route_success

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
        self.last_report = report

        self.total_reports_sent += 1

        response = self.http.generate_report(report)

        self._log(
            "report",
            response is not None,
            report
        )

        return response
    
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
        
        camera_payload["size_bytes"] = len(buffer)

        camera_payload["encoding"] = "jpg"

        camera_payload["timestamp"] = datetime.now().isoformat()

        self.total_frames_sent += 1

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
    # Health
    # =====================================================

    def health(self):

        return {

            "websocket": self.websocket.connected,

            "messages_sent": self.messages_sent,

            "messages_failed": self.messages_failed,

            "last_transmission": self.last_transmission,

            "started_at": self.started_at.isoformat()

        }
    
    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "messages_sent": self.messages_sent,

            "messages_failed": self.messages_failed,

            "websocket_messages": self.websocket_messages,

            "http_messages": self.http_messages,

            "frames": self.total_frames_sent,

            "detections": self.total_detections_sent,

            "statistics": self.total_statistics_sent,

            "alerts": self.total_alerts_sent,

            "reports": self.total_reports_sent

        }

    def latest(self):

        return {

            "statistics": self.last_statistics,

            "detection": self.last_detection,

            "alert": self.last_alert,

            "route": self.last_route,

            "report": self.last_report

        }

    def transmission_history(self):

        return list(self.history)
    
    def info(self):

        return {

            "module":"Output Manager",

            "status":"Running",

            "history_size":len(self.history),

            "websocket_connected":self.websocket.connected,

            "http_client":"Ready",

            "started_at":self.started_at.isoformat()

        }
    
    def reset(self):

        self.history.clear()

        self.messages_sent = 0

        self.messages_failed = 0

        self.websocket_messages = 0

        self.http_messages = 0

        self.total_frames_sent = 0

        self.total_statistics_sent = 0

        self.total_alerts_sent = 0

        self.total_detections_sent = 0

        self.total_reports_sent = 0

        self.last_statistics = None

        self.last_detection = None

        self.last_alert = None

        self.last_route = None

        self.last_report = None

    def dashboard(self):

        return {

            "connected": self.websocket.connected,

            "messages_sent": self.messages_sent,

            "messages_failed": self.messages_failed,

            "frames": self.total_frames_sent,

            "alerts": self.total_alerts_sent,

            "detections": self.total_detections_sent,

            "statistics": self.total_statistics_sent,

            "last_transmission": self.last_transmission

        }

    def retry_http(

        self,

        endpoint,

        payload,

        retries=3

    ):

        for _ in range(retries):

            response = self.http._request(

                "POST",

                endpoint,

                payload

            )

            if response is not None:

                return response

        return None

    def connectivity(self):

        backend = self.http.ping()

        return {

            "http": backend is not None,

            "websocket": self.websocket.connected

        }

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

        self._log(
            "shutdown",
            True,
            {
                "messages_sent": self.messages_sent,
                "frames_sent": self.total_frames_sent
            }
        )

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