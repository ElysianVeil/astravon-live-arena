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

        self.connecting = False

        self.url = settings.WEBSOCKET_URL

    # ========================================================
    # Connection
    # ========================================================

    async def connect(self) -> bool:
        """
        Connects to the backend.
        """

        if self.connected and self.websocket is not None:
            return True

        if self.connecting:
            return False

        self.connecting = True

        try:

            self.websocket = await websockets.connect(
                self.url,
                ping_interval=20,
                ping_timeout=20,
                close_timeout=5,
            )

            self.connected = True

            logger.info("Connected to backend WebSocket.")

            return True

        except Exception as error:

            logger.error(f"Connection failed: {error}")

            self.connected = False

            self.websocket = None

            return False

        finally:

            self.connecting = False

    async def disconnect(self) -> None:
        """
        Disconnects from the backend.
        """

        if self.websocket is None:

            return

        try:

            await asyncio.wait_for(
                self.websocket.close(),
                timeout=5
            )

        except Exception as error:

            logger.warning(
                f"WebSocket shutdown: {error}"
            )

        finally:

            self.websocket = None

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

        if not self.connected:

            success = await self.connect()

            if not success:

                return False

        try:
            print("WS SEND:", message["type"])

            await self.websocket.send(
                json.dumps(message)
            )

            print("WS SENT")

            return True

        except Exception as error:

            logger.error(error)

            self.connected = False

            self.websocket = None

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
    
    async def send_camera_frame(self, payload):

        await self.send({
            "type": "frame",
            "data": payload
        })


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