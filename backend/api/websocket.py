"""
============================================================
Astravon Live Arena
WebSocket Manager

Purpose:
    Manages real-time communication between the backend
    and connected dashboard clients.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import List
import asyncio
from collections import deque
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
from backend.utils.logger import get_logger

logger = get_logger("WebSocketManager")

# ============================================================
# Router
# ============================================================

router = APIRouter(
    tags=["WebSocket"]
)

class LiveState:
    # latest_statistics = None
    # latest_frame = None
    recent_frames = deque(
        maxlen=5
    )
    recent_detections = deque(
        maxlen=20
    )
    recent_statistics = deque(
        maxlen=20
    )
    recent_alerts = deque(
        maxlen=50
    )
    recent_events = deque(
        maxlen=20
    )

    engine_status = {
        "connected": False,
        "last_message": None
    }
    # latest_alert = None
    # latest_detection = None
    # latest_event = None

    @classmethod
    def update(cls, message: dict):

        message_type = message.get("type")

        if message_type == "statistics":
            cls.recent_statistics.append(message)

        elif message_type == "frame":
            cls.recent_frames.append(message)

        elif message_type == "alert":
            cls.recent_alerts.append(message)

        elif message_type == "detection":
            cls.recent_detections.append(message)

        elif message_type == "event":
            cls.recent_events.append(message)

    @classmethod
    async def sync(cls, websocket: WebSocket):

        for stat in cls.recent_statistics:
            await websocket.send_json(stat)

        for frame in cls.recent_frames:
            await websocket.send_json(frame)

        for detection in cls.recent_detections:
            await websocket.send_json(detection)

        for alert in cls.recent_alerts:
            await websocket.send_json(alert)

        for event in cls.recent_events:
            await websocket.send_json(event)

# ============================================================
# Connection Manager
# ============================================================

class ConnectionManager:
    """
    Handles all active websocket connections.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_info = {}
        LiveState.engines = {}

    async def connect(self, websocket: WebSocket):
        """
        Accept a new websocket connection.
        """
        client_id = uuid.uuid4().hex

        await websocket.accept()
        self.connection_info[websocket] = {

            "connected_at": datetime.utcnow().isoformat(),

            "messages_sent": 0,

            "client": str(websocket.client)

        }
        self.connection_info[websocket]["id"] = client_id

        self.active_connections.append(websocket)

        await websocket.send_json({

            "type":"connected",

            "client_id": client_id

        })

        print(
            f"[WebSocket] Client Connected "
            f"({len(self.active_connections)} active)"
        )

    def disconnect(self, websocket: WebSocket):
        """
        Remove a disconnected client.
        """

        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.connection_info.pop(
                websocket,
                None
            )

        print(
            f"[WebSocket] Client Disconnected "
            f"({len(self.active_connections)} active)"
        )

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket
    ):
        """
        Send data to one client.
        """

        await websocket.send_json(message)

    async def broadcast(
        self,
        message: dict
    ):
        """
        Send data to all connected clients.
        """

        disconnected = []

        for connection in self.active_connections:

            try:

                await connection.send_json(message)

                info = self.connection_info.get(connection)

                if info:
                    info["messages_sent"] += 1

            except Exception:

                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_detection(
        self,
        detection
    ):
        await self.broadcast({
            "type":"detection",
            "data": detection
        })

    async def heartbeat():

        while True:

            await asyncio.sleep(30)

            await manager.broadcast({

                "type":"heartbeat",

                "timestamp": datetime.utcnow().isoformat()

            })

    def connection_count(self) -> int:
        """
        Returns number of active clients.
        """

        return len(self.active_connections)


# ============================================================
# Global Manager
# ============================================================

manager = ConnectionManager()

@router.websocket("/ws/engine")
async def engine_socket(websocket: WebSocket):

    await websocket.accept()

    LiveState.engine_status = {
        "connected": True,
        "last_message": datetime.utcnow().isoformat()
    }

    logger.info("AI Engine Connected")

    # asyncio.create_task(
    #     self.heartbeat()
    # )

    print("AI Engine Connected")

    try:

        while True:

            message = await websocket.receive_json()

            if message.get("type") == "ping":

                await websocket.send_json({

                    "type":"pong",

                    "timestamp":

                        datetime.utcnow().isoformat()

                })

                continue

            message_type = message.get("type")

            if message_type not in {
                "statistics",
                "detection",
                "frame",
                "alert",
                "event",
                "system",
                "heartbeat"
            }:
                continue

            payload = message.get("data")

            if payload is None:
                continue
            

            LiveState.update(message)

            LiveState.engine_status = {

                "last_message": datetime.utcnow(),

                "connected": True

            }

            message.setdefault(

                "timestamp",

                datetime.utcnow().isoformat()

            )

            await manager.broadcast(message)

    except WebSocketDisconnect:

        LiveState.engine_status["connected"] = False

        print("AI Engine Disconnected")


# ============================================================
# WebSocket Endpoint
# ============================================================

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):
    """
    Main websocket endpoint.
    """

    await manager.connect(websocket)

    await LiveState.sync(websocket)

    try:

        while True:

            await asyncio.sleep(30)

    except WebSocketDisconnect:

        manager.disconnect(websocket)

    except Exception as error:

        manager.disconnect(websocket)

        logger.exception(

            "WebSocket failure"

        )


# ============================================================
# Helper Functions
# ============================================================

async def broadcast_statistics(
    people_count: int,
    density: str,
    temperature: float,
    risk_score: int
):
    """
    Broadcast dashboard statistics.
    """

    await manager.broadcast(
        {
            "type": "statistics",

            "success": True,

            "data": {
                "people_count": people_count,
                "density": density,
                "temperature": temperature,
                "risk_score": risk_score
            }
        }
    )


async def broadcast_alert(
    title: str,
    severity: str,
    description: str
):
    """
    Broadcast an alert.
    """

    await manager.broadcast(
        {
            "type": "alert",

            "success": True,

            "data": {
                "title": title,
                "severity": severity,
                "description": description
            }
        }
    )


async def broadcast_event_status(
    status: str
):
    """
    Broadcast event status updates.
    """

    await manager.broadcast(
        {
            "type": "event",

            "success": True,

            "data": {
                "status": status
            }
        }
    )


async def broadcast_system_message(
    message: str
):
    """
    Broadcast a general system message.
    """

    await manager.broadcast(
        {
            "type": "system",

            "success": True,

            "data": {
                "message": message
            }
        }
    )


# ============================================================
# Connection Information
# ============================================================

def active_connections():
    """
    Returns connection statistics.
    """

    return {

        "active_connections":

            manager.connection_count(),

        "engine_connected":

            LiveState.engine_status["connected"],

        "messages_sent":

            sum(

                x["messages_sent"]

                for x

                in manager.connection_info.values()

            )

    }