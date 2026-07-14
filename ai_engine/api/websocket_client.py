"""
============================================================
Astravon Live Arena
WebSocket Client

Purpose:
    Sends real-time AI updates to the backend
    through a WebSocket connection.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, Optional

import websockets

from config import settings


# ============================================================
# Logger
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# WebSocket Client
# ============================================================

class WebSocketClient:
    """
    WebSocket client for communicating with the backend.
    """

    def __init__(self) -> None:

        self.websocket: Optional[websockets.ClientConnection] = None

        self.connected = False

        self.url = settings.WEBSOCKET_URL

    # ========================================================
    # Connection
    # ========================================================

    async def connect(self) -> bool:
        """
        Connects to the backend.
        """

        try:

            self.websocket = await websockets.connect(
                self.url
            )

            self.connected = True

            logger.info(
                "Connected to backend WebSocket."
            )

            return True

        except Exception as error:

            logger.error(
                f"WebSocket connection failed: {error}"
            )

            self.connected = False

            return False

    async def disconnect(self) -> None:
        """
        Disconnects from the backend.
        """

        if self.websocket:

            await self.websocket.close()

        self.connected = False

        logger.info(
            "Disconnected from backend."
        )

    # ========================================================
    # Generic Sender
    # ========================================================

    async def send(
        self,
        message: Dict[str, Any]
    ) -> bool:
        """
        Sends a JSON message.
        """

        try:

            if not self.connected:
                await self.connect()

            if self.websocket is None:
                return False

            await self.websocket.send(
                json.dumps(message)
            )

            return True

        except Exception as error:

            logger.error(error)

            self.connected = False

            return False

    # ========================================================
    # Statistics
    # ========================================================

    async def send_statistics(
        self,
        statistics: Dict[str, Any]
    ) -> bool:

        return await self.send(
            {
                "type": "statistics",
                "data": statistics
            }
        )

    # ========================================================
    # Detection
    # ========================================================

    async def send_detection(
        self,
        detection: Dict[str, Any]
    ) -> bool:

        return await self.send(
            {
                "type": "detection",
                "data": detection
            }
        )

    # ========================================================
    # Alert
    # ========================================================

    async def send_alert(
        self,
        alert: Dict[str, Any]
    ) -> bool:

        return await self.send(
            {
                "type": "alert",
                "data": alert
            }
        )

    # ========================================================
    # Route
    # ========================================================

    async def send_route(
        self,
        route: Dict[str, Any]
    ) -> bool:

        return await self.send(
            {
                "type": "route",
                "data": route
            }
        )

    # ========================================================
    # Heartbeat
    # ========================================================

    async def heartbeat(self) -> bool:
        """
        Sends a heartbeat.
        """

        return await self.send(
            {
                "type": "heartbeat"
            }
        )


# ============================================================
# Demonstration
# ============================================================

async def main():

    client = WebSocketClient()

    await client.connect()

    await client.send_statistics(
        {
            "people_count": 152,
            "density": "Medium",
            "temperature": 31.6,
            "risk_score": 45
        }
    )

    await asyncio.sleep(2)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())