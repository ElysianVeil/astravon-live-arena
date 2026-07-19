"""
============================================================
Astravon Live Arena
WebSocket Manager

Purpose:
    Centralized management of all WebSocket clients.

Responsibilities:
    • Manage frontend dashboard connections
    • Multi-camera subscriptions
    • Broadcast events
    • Send camera-specific events
    • Heartbeat support
    • Automatic disconnect cleanup
    • Thread-safe asyncio implementation

Author:
    House of Astravon

Version:
    2.0.0
============================================================
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import datetime
from typing import Dict, Set, Optional

from fastapi import WebSocket
from utils.logger import get_logger

logger = get_logger("WebSocketManager")


# ============================================================
# WebSocket Manager
# ============================================================

class WebSocketManager:

    def __init__(self):

        # websocket_id -> websocket
        self._connections: Dict[int, WebSocket] = {}

        # camera_id -> websocket ids
        self._subscriptions: Dict[str, Set[int]] = defaultdict(set)

        self._lock = asyncio.Lock()

        logger.info("WebSocket Manager initialized.")

    # ========================================================
    # Connection
    # ========================================================

    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        async with self._lock:

            self._connections[id(websocket)] = websocket

        logger.info(
            f"Dashboard connected ({len(self._connections)})"
        )

    async def disconnect(
        self,
        websocket: WebSocket
    ):

        async with self._lock:

            wsid = id(websocket)

            self._connections.pop(
                wsid,
                None
            )

            for camera in self._subscriptions.values():

                camera.discard(wsid)

        logger.info(
            f"Dashboard disconnected ({len(self._connections)})"
        )

    # ========================================================
    # Camera Subscription
    # ========================================================

    async def subscribe(
        self,
        websocket: WebSocket,
        camera_id: str
    ):

        async with self._lock:

            self._subscriptions[camera_id].add(
                id(websocket)
            )

        logger.info(
            f"Subscribed -> {camera_id}"
        )

    async def unsubscribe(
        self,
        websocket: WebSocket,
        camera_id: str
    ):

        async with self._lock:

            self._subscriptions[camera_id].discard(
                id(websocket)
            )

        logger.info(
            f"Unsubscribed -> {camera_id}"
        )

    # ========================================================
    # Broadcast
    # ========================================================

    async def broadcast(
        self,
        message: dict
    ):

        dead = []

        async with self._lock:

            for wsid, websocket in self._connections.items():

                try:

                    await websocket.send_json(message)

                except Exception:

                    dead.append(wsid)

        await self._cleanup(dead)

    # ========================================================
    # Camera Broadcast
    # ========================================================

    async def broadcast_camera(
        self,
        camera_id: str,
        message: dict
    ):

        dead = []

        async with self._lock:

            ids = self._subscriptions.get(
                camera_id,
                set()
            )

            for wsid in ids:

                websocket = self._connections.get(wsid)

                if websocket is None:
                    continue

                try:

                    await websocket.send_json(message)

                except Exception:

                    dead.append(wsid)

        await self._cleanup(dead)

    # ========================================================
    # Detection
    # ========================================================

    async def send_detection(
        self,
        camera_id: str,
        detections: list
    ):

        await self.broadcast_camera(

            camera_id,

            {

                "type": "detection",

                "camera": camera_id,

                "timestamp": datetime.utcnow().isoformat(),

                "detections": detections

            }

        )

    # ========================================================
    # Statistics
    # ========================================================

    async def send_statistics(
        self,
        camera_id: str,
        statistics: dict
    ):

        await self.broadcast_camera(

            camera_id,

            {

                "type": "statistics",

                "camera": camera_id,

                "timestamp": datetime.utcnow().isoformat(),

                "statistics": statistics

            }

        )

    # ========================================================
    # Alerts
    # ========================================================

    async def send_alert(
        self,
        camera_id: str,
        alert: dict
    ):

        await self.broadcast_camera(

            camera_id,

            {

                "type": "alert",

                "camera": camera_id,

                "timestamp": datetime.utcnow().isoformat(),

                "alert": alert

            }

        )

    # ========================================================
    # Frame Metadata
    # ========================================================

    async def send_frame_info(
        self,
        camera_id: str,
        frame_number: int,
        fps: float
    ):

        await self.broadcast_camera(

            camera_id,

            {

                "type": "frame",

                "camera": camera_id,

                "frame": frame_number,

                "fps": fps,

                "timestamp": datetime.utcnow().isoformat()

            }

        )

    # ========================================================
    # Heartbeat
    # ========================================================

    async def heartbeat(self):

        await self.broadcast(

            {

                "type": "heartbeat",

                "timestamp": datetime.utcnow().isoformat()

            }

        )

    # ========================================================
    # Cleanup
    # ========================================================

    async def _cleanup(
        self,
        dead_connections
    ):

        if not dead_connections:
            return

        async with self._lock:

            for wsid in dead_connections:

                self._connections.pop(
                    wsid,
                    None
                )

                for subscribers in self._subscriptions.values():

                    subscribers.discard(wsid)

        logger.info(
            f"Removed {len(dead_connections)} dead websocket(s)"
        )

    # ========================================================
    # Information
    # ========================================================

    def info(self):

        return {

            "connections": len(self._connections),

            "subscriptions": {

                camera: len(clients)

                for camera, clients

                in self._subscriptions.items()

            }

        }

    @property
    def total_connections(self):

        return len(self._connections)

    @property
    def total_subscriptions(self):

        return sum(

            len(v)

            for v

            in self._subscriptions.values()

        )

    # ========================================================
    # Reset
    # ========================================================

    async def reset(self):

        async with self._lock:

            self._connections.clear()

            self._subscriptions.clear()

        logger.info(
            "WebSocket Manager reset."
        )