"""
============================================================
Astravon Live Arena
Camera Service

Purpose:
    Business logic for managing cameras.

Responsibilities:
    - Register cameras
    - Update camera status
    - Retrieve cameras
    - Remove cameras
    - Bridge managers and storage/database

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from models.camera import Camera

# try:
#     # Future database support
#     from sqlalchemy.orm import Session
# except Exception:
#     Session = None


class CameraService:
    """
    Camera business logic.

    The service is intentionally isolated from
    FastAPI endpoints so it can later be reused by

        • API
        • WebSocket
        • AI Engine
        • Scheduler
        • CLI
    """

    # def __init__(self, db: Optional[Session] = None):

    #     self.db = db

    # ========================================================
    # Create
    # ========================================================

    def register_camera(

        self,

        camera_id: str,

        name: str,

        source: str,

        location: str = "",

        source_type: str = "webcam",

        resolution: str = "1280x720",

        fps_limit: int = 30

    ) -> Camera:

        camera = Camera(

            camera_id=camera_id,

            name=name,

            source=source,

            location=location,

            source_type=source_type,

            resolution=resolution,

            fps_limit=fps_limit

        )

        if self.db:

            self.db.add(camera)
            self.db.commit()
            self.db.refresh(camera)

        return camera

    # ========================================================
    # Read
    # ========================================================

    def get_camera(

        self,

        camera_id: str

    ) -> Optional[Camera]:

        if self.db is None:

            return None

        return (

            self.db.query(Camera)

            .filter(

                Camera.camera_id == camera_id

            )

            .first()

        )

    def get_all_cameras(

        self

    ) -> List[Camera]:

        if self.db is None:

            return []

        return (

            self.db.query(Camera)

            .order_by(Camera.name)

            .all()

        )

    def get_connected_cameras(

        self

    ) -> List[Camera]:

        if self.db is None:

            return []

        return (

            self.db.query(Camera)

            .filter(

                Camera.connected == True

            )

            .all()

        )

    # ========================================================
    # Update
    # ========================================================

    def connect_camera(

        self,

        camera_id: str

    ) -> Optional[Camera]:

        camera = self.get_camera(camera_id)

        if camera is None:

            return None

        camera.connected = True
        camera.active = True
        camera.connected_at = datetime.utcnow()

        self.db.commit()

        return camera

    def disconnect_camera(

        self,

        camera_id: str

    ) -> Optional[Camera]:

        camera = self.get_camera(camera_id)

        if camera is None:

            return None

        camera.connected = False
        camera.active = False
        camera.disconnected_at = datetime.utcnow()

        self.db.commit()

        return camera

    def update_statistics(

        self,

        camera_id: str,

        fps: float,

        people: int,

        congestion: float,

        risk: float,

        dropped_frames: int = 0,

        total_frames: int = 0

    ) -> Optional[Camera]:

        camera = self.get_camera(camera_id)

        if camera is None:

            return None

        camera.current_fps = fps
        camera.people_count = people
        camera.congestion_score = congestion
        camera.risk_score = risk
        camera.dropped_frames = dropped_frames
        camera.total_frames = total_frames
        camera.last_frame_at = datetime.utcnow()

        self.db.commit()

        return camera

    # ========================================================
    # Enable / Disable
    # ========================================================

    def enable_camera(

        self,

        camera_id: str

    ) -> bool:

        camera = self.get_camera(camera_id)

        if camera is None:

            return False

        camera.enabled = True

        self.db.commit()

        return True

    def disable_camera(

        self,

        camera_id: str

    ) -> bool:

        camera = self.get_camera(camera_id)

        if camera is None:

            return False

        camera.enabled = False

        self.db.commit()

        return True

    # ========================================================
    # Delete
    # ========================================================

    def delete_camera(

        self,

        camera_id: str

    ) -> bool:

        camera = self.get_camera(camera_id)

        if camera is None:

            return False

        self.db.delete(camera)

        self.db.commit()

        return True

    # ========================================================
    # Dashboard
    # ========================================================

    def dashboard_summary(self):

        cameras = self.get_all_cameras()

        connected = sum(

            1

            for c in cameras

            if c.connected

        )

        active = sum(

            1

            for c in cameras

            if c.active

        )

        total_people = sum(

            c.people_count

            for c in cameras

        )

        average_risk = 0.0

        if cameras:

            average_risk = (

                sum(

                    c.risk_score

                    for c in cameras

                )

                / len(cameras)

            )

        return {

            "registered_cameras": len(cameras),

            "connected_cameras": connected,

            "active_cameras": active,

            "total_people": total_people,

            "average_risk": round(

                average_risk,

                2

            )

        }