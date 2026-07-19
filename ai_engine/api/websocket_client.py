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
import cv2
import base64
import logging
from datetime import datetime
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
        # Runtime Statistics
        # ========================================================

        self.messages_sent = 0

        self.messages_failed = 0

        self.bytes_sent = 0

        self.last_message = None

        self.last_connected = None

        self.last_heartbeat = None

        self.reconnect_attempts = 0

        self.maximum_reconnect_attempts = 10

        self.auto_reconnect = True

        self.connection_timeout = 10

        self.send_queue = asyncio.Queue()

        self.running = False

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

        self.last_connected = datetime.utcnow().isoformat()

        self.reconnect_attempts = 0

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

            self.reconnect_attempts += 1

            logger.error(
                f"Connection failed ({self.reconnect_attempts}): {error}"
            )

            self.connected = False

            self.websocket = None

            if (

                self.auto_reconnect

                and

                self.reconnect_attempts

                <

                self.maximum_reconnect_attempts

            ):

                await asyncio.sleep(2)

                return await self.connect()

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

            payload = json.dumps(message)

            await self.websocket.send(payload)

            self.messages_sent += 1

            self.bytes_sent += len(payload)

            self.last_message = message["type"]

            return True


        except Exception as error:

            self.messages_failed += 1

            logger.error(error)

            self.connected = False

            self.websocket = None

            if self.auto_reconnect:

                await self.connect()

            return False
        
    # ========================================================
    # Queue Worker
    # ========================================================

    async def process_queue(self):

        self.running = True

        while self.running:

            message = await self.send_queue.get()

            try:

                await self.send(message)

            finally:

                self.send_queue.task_done()

    # ========================================================
    # Queue Message
    # ========================================================

    async def enqueue(

        self,

        message

    ):

        await self.send_queue.put(message)

    # ========================================================
    # Batch Send
    # ========================================================

    async def send_batch(

        self,

        messages

    ):

        for message in messages:

            await self.enqueue(message)

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

        self.last_heartbeat = datetime.utcnow().isoformat()

        return await self.send(

            {

                "type":"heartbeat",

                "timestamp":self.last_heartbeat

            }

        )
    
    # ========================================================
    # Ping
    # ========================================================

    async def ping(self):

        return await self.send(

            {

                "type":"ping"

            }

        )
    
    # ========================================================
    # Pong
    # ========================================================

    async def pong(self):

        return await self.send(

            {

                "type":"pong"

            }

        )

    async def send_camera_frame(self, payload):

        await self.send({
            "type": "frame",
            "data": payload
        })

    # ========================================================
    # Register Camera
    # ========================================================

    async def register_camera(

        self,

        camera

    ):

        await self.send(

            {

                "type":"camera_register",

                "data":camera

            }

        )

    # ========================================================
    # Camera Status
    # ========================================================

    async def send_camera_status(

        self,

        status

    ):

        await self.send(

            {

                "type":"camera_status",

                "data":status

            }

        )


    # ========================================================
    # Engine Status
    # ========================================================

    async def send_engine_status(

        self,

        status

    ):

        await self.send(

            {

                "type":"engine_status",

                "data":status

            }

        )

    # ========================================================
    # Weather
    # ========================================================

    async def send_weather(

        self,

        weather

    ):

        await self.send(

            {

                "type":"weather",

                "data":weather

            }

        )

    # ========================================================
    # Prediction
    # ========================================================

    async def send_prediction(

        self,

        prediction

    ):

        await self.send(

            {

                "type":"prediction",

                "data":prediction

            }

        )

    # ========================================================
    # Metrics
    # ========================================================

    async def send_metrics(

        self,

        metrics

    ):

        await self.send(

            {

                "type":"metrics",

                "data":metrics

            }

        )

    # ========================================================
    # Module Information
    # ========================================================

    def info(self):

        return {

            "module":"WebSocket Client",

            "status":(

                "Connected"

                if self.connected

                else "Disconnected"

            ),

            "url":self.url,

            "messages_sent":self.messages_sent,

            "messages_failed":self.messages_failed,

            "bytes_sent":self.bytes_sent,

            "queue_size":self.send_queue.qsize(),

            "last_message":self.last_message,

            "last_connected":self.last_connected,

            "last_heartbeat":self.last_heartbeat,

            "reconnect_attempts":self.reconnect_attempts

        }

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):

        success_rate = 100

        total = self.messages_sent + self.messages_failed

        if total:

            success_rate = round(

                self.messages_sent

                /

                total

                *

                100,

                2

            )

        return {

            "messages_sent":self.messages_sent,

            "messages_failed":self.messages_failed,

            "success_rate":success_rate,

            "bytes_sent":self.bytes_sent

        }

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):

        self.messages_sent = 0

        self.messages_failed = 0

        self.bytes_sent = 0

        self.last_message = None

        self.last_connected = None

        self.last_heartbeat = None

        self.reconnect_attempts = 0

    # ========================================================
    # Shutdown
    # ========================================================

    async def shutdown(self):

        self.running = False

        await self.disconnect()

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