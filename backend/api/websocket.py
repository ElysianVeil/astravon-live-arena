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

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# ============================================================
# Router
# ============================================================

router = APIRouter(
    tags=["WebSocket"]
)

class LiveState:
    latest_statistics = None
    latest_frame = None
    latest_alert = None
    latest_detection = None
    latest_event = None

    @classmethod
    def update(cls, message: dict):

        message_type = message.get("type")

        if message_type == "statistics":
            cls.latest_statistics = message

        elif message_type == "frame":
            cls.latest_frame = message

        elif message_type == "alert":
            cls.latest_alert = message

        elif message_type == "detection":
            cls.latest_detection = message

        elif message_type == "event":
            cls.latest_event = message

    @classmethod
    async def sync(cls, websocket: WebSocket):

        if cls.latest_statistics:
            await websocket.send_json(cls.latest_statistics)

        if cls.latest_frame:
            await websocket.send_json(cls.latest_frame)

        if cls.latest_detection:
            await websocket.send_json(cls.latest_detection)

        if cls.latest_alert:
            await websocket.send_json(cls.latest_alert)

        if cls.latest_event:
            await websocket.send_json(cls.latest_event)

# ============================================================
# Connection Manager
# ============================================================

class ConnectionManager:
    """
    Handles all active websocket connections.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accept a new websocket connection.
        """

        await websocket.accept()

        self.active_connections.append(websocket)

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

            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)

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

    print("AI Engine Connected")

    try:

        while True:

            message = await websocket.receive_json()

            LiveState.update(message)

            await manager.broadcast(message)

    except WebSocketDisconnect:

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

        print(f"WebSocket Error: {error}")


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
        "active_connections": manager.connection_count()
    }