"""
============================================================
Astravon Live Arena
Camera Manager

Purpose:
    Centralized manager responsible for all connected cameras.

Responsibilities:
    • Register cameras
    • Remove cameras
    • Update camera status
    • Store latest frame
    • Store latest statistics
    • Store latest alerts
    • Camera health monitoring
    • Thread-safe access

Author:
    House of Astravon

Version:
    2.0.0
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from datetime import datetime
from typing import Dict, Optional, List, Any

from utils.logger import get_logger

logger = get_logger("CameraManager")


# ============================================================
# Camera State
# ============================================================

@dataclass
class CameraState:
    """
    Represents one live camera.
    """

    camera_id: str
    name: str

    connected: bool = True

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    latest_frame: Optional[bytes] = None

    statistics: Dict[str, Any] = field(default_factory=dict)

    alerts: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    fps: float = 0.0

    inference_time: float = 0.0

    ai_status: str = "Running"

    health: str = "Healthy"


# ============================================================
# Camera Manager
# ============================================================

class CameraManager:

    def __init__(self):

        self._lock = Lock()

        self._cameras: Dict[str, CameraState] = {}

        logger.info("Camera Manager initialized.")

    # --------------------------------------------------------
    # Registration
    # --------------------------------------------------------

    def register_camera(
        self,
        camera_id: str,
        name: str,
        metadata: Optional[Dict] = None
    ) -> CameraState:

        with self._lock:

            if camera_id in self._cameras:

                logger.warning(
                    f"Camera already exists: {camera_id}"
                )

                return self._cameras[camera_id]

            state = CameraState(

                camera_id=camera_id,

                name=name,

                metadata=metadata or {}

            )

            self._cameras[camera_id] = state

            logger.info(
                f"Registered camera: {camera_id}"
            )

            return state

    # --------------------------------------------------------
    # Remove Camera
    # --------------------------------------------------------

    def remove_camera(
        self,
        camera_id: str
    ):

        with self._lock:

            if camera_id in self._cameras:

                del self._cameras[camera_id]

                logger.info(
                    f"Removed camera: {camera_id}"
                )

    # --------------------------------------------------------
    # Connection
    # --------------------------------------------------------

    def set_connected(
        self,
        camera_id: str,
        connected: bool
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.connected = connected

            camera.updated_at = datetime.utcnow()

    # --------------------------------------------------------
    # Frame
    # --------------------------------------------------------

    def update_frame(
        self,
        camera_id: str,
        frame: bytes
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.latest_frame = frame

            camera.updated_at = datetime.utcnow()

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def update_statistics(
        self,
        camera_id: str,
        statistics: Dict
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.statistics = statistics

            camera.updated_at = datetime.utcnow()

    # --------------------------------------------------------
    # Alerts
    # --------------------------------------------------------

    def add_alert(
        self,
        camera_id: str,
        alert: Dict
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.alerts.append(alert)

            camera.updated_at = datetime.utcnow()

    # --------------------------------------------------------
    # Performance
    # --------------------------------------------------------

    def update_metrics(
        self,
        camera_id: str,
        fps: float,
        inference_time: float
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.fps = fps

            camera.inference_time = inference_time

            camera.updated_at = datetime.utcnow()

    # --------------------------------------------------------
    # AI Status
    # --------------------------------------------------------

    def set_ai_status(
        self,
        camera_id: str,
        status: str
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.ai_status = status

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    def set_health(
        self,
        camera_id: str,
        health: str
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.health = health

    # --------------------------------------------------------
    # Get One
    # --------------------------------------------------------

    def get(
        self,
        camera_id: str
    ) -> Optional[CameraState]:

        return self._cameras.get(camera_id)

    # --------------------------------------------------------
    # Latest Frame
    # --------------------------------------------------------

    def latest_frame(
        self,
        camera_id: str
    ) -> Optional[bytes]:

        camera = self.get(camera_id)

        if camera is None:

            return None

        return camera.latest_frame

    # --------------------------------------------------------
    # Camera List
    # --------------------------------------------------------

    def list_cameras(self):

        return list(self._cameras.values())

    # --------------------------------------------------------
    # IDs
    # --------------------------------------------------------

    def ids(self):

        return list(self._cameras.keys())

    # --------------------------------------------------------
    # Count
    # --------------------------------------------------------

    @property
    def count(self):

        return len(self._cameras)

    # --------------------------------------------------------
    # Snapshot
    # --------------------------------------------------------

    def snapshot(self):

        data = {}

        for camera in self._cameras.values():

            data[camera.camera_id] = {

                "name": camera.name,

                "connected": camera.connected,

                "fps": camera.fps,

                "inference_time": camera.inference_time,

                "health": camera.health,

                "ai_status": camera.ai_status,

                "statistics": camera.statistics,

                "alerts": len(camera.alerts),

                "updated_at": camera.updated_at.isoformat()

            }

        return data

    # --------------------------------------------------------
    # Clear Alerts
    # --------------------------------------------------------

    def clear_alerts(
        self,
        camera_id: str
    ):

        camera = self.get(camera_id)

        if camera is None:
            return

        with self._lock:

            camera.alerts.clear()

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(self):

        with self._lock:

            self._cameras.clear()

            logger.info("Camera Manager reset.")