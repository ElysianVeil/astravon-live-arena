"""
============================================================
Astravon Live Arena
Notification Service

Purpose:
    Centralized notification service responsible for
    delivering alerts throughout the Astravon Live Arena
    platform.

Supports:
    - WebSocket notifications
    - Console notifications
    - JSON archive
    - Email (future)
    - SMS (future)
    - Push notifications (future)

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from utils.logger import get_logger

logger = get_logger("Notification Service")


class NotificationService:
    """
    Sends notifications to various delivery channels.

    This service is intentionally independent from
    AlertManager so future delivery methods can be
    added without modifying alert generation logic.
    """

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(

        self,

        websocket_manager=None,

        archive_storage=None

    ):

        self.websocket_manager = websocket_manager

        self.archive_storage = archive_storage

    # ==========================================================
    # Generic Notification
    # ==========================================================

    async def notify(

        self,

        title: str,

        message: str,

        severity: str = "info",

        camera_id: Optional[str] = None,

        payload: Optional[Dict] = None

    ) -> Dict:

        notification = {

            "title": title,

            "message": message,

            "severity": severity,

            "camera_id": camera_id,

            "payload": payload or {},

            "timestamp": datetime.utcnow().isoformat()

        }

        logger.info(

            f"[{severity.upper()}] "

            f"{title}"

        )

        # --------------------------------------
        # WebSocket Broadcast
        # --------------------------------------

        if self.websocket_manager:

            try:

                await self.websocket_manager.broadcast(

                    "notification",

                    notification

                )

            except Exception as e:

                logger.warning(

                    f"WebSocket notification failed: {e}"

                )

        # --------------------------------------
        # Archive
        # --------------------------------------

        if self.archive_storage:

            try:

                self.archive_storage.save_notification(

                    notification

                )

            except Exception as e:

                logger.warning(

                    f"Notification archive failed: {e}"

                )

        return notification

    # ==========================================================
    # Alert Notification
    # ==========================================================

    async def send_alert(

        self,

        alert: Dict

    ):

        return await self.notify(

            title=alert.get(

                "title",

                "Alert"

            ),

            message=alert.get(

                "message",

                ""

            ),

            severity=alert.get(

                "severity",

                "medium"

            ),

            camera_id=alert.get(

                "camera_id"

            ),

            payload=alert

        )

    # ==========================================================
    # Camera Notification
    # ==========================================================

    async def camera_connected(

        self,

        camera_name: str

    ):

        return await self.notify(

            title="Camera Connected",

            message=f"{camera_name} is online.",

            severity="info"

        )

    async def camera_disconnected(

        self,

        camera_name: str

    ):

        return await self.notify(

            title="Camera Disconnected",

            message=f"{camera_name} has disconnected.",

            severity="warning"

        )

    # ==========================================================
    # AI Notifications
    # ==========================================================

    async def ai_started(self):

        return await self.notify(

            title="AI Engine Started",

            message="Astravon AI Engine is running.",

            severity="info"

        )

    async def ai_stopped(self):

        return await self.notify(

            title="AI Engine Stopped",

            message="Astravon AI Engine has stopped.",

            severity="warning"

        )

    # ==========================================================
    # Emergency Notification
    # ==========================================================

    async def emergency(

        self,

        title: str,

        message: str,

        payload: Optional[Dict] = None

    ):

        return await self.notify(

            title=title,

            message=message,

            severity="critical",

            payload=payload

        )

    # ==========================================================
    # Statistics Notification
    # ==========================================================

    async def statistics_update(

        self,

        statistics: Dict

    ):

        if self.websocket_manager:

            await self.websocket_manager.broadcast(

                "statistics",

                statistics

            )

    # ==========================================================
    # Detection Notification
    # ==========================================================

    async def detections(

        self,

        detections: List[Dict]

    ):

        if self.websocket_manager:

            await self.websocket_manager.broadcast(

                "detections",

                detections

            )

    # ==========================================================
    # Heartbeat
    # ==========================================================

    async def heartbeat(self):

        if self.websocket_manager:

            await self.websocket_manager.broadcast(

                "heartbeat",

                {

                    "status": "alive",

                    "timestamp":

                        datetime.utcnow().isoformat()

                }

            )