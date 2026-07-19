"""
============================================================
Astravon Live Arena
Camera Model

Purpose:
    Represents a camera connected to the Astravon Live Arena
    backend. This model is shared between the managers,
    services, websocket layer, and storage.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class Camera:
    """
    Camera model.

    Example
    -------
    Camera(
        camera_id="cam_001",
        name="Main Entrance",
        source=0
    )
    """

    # =====================================================
    # Identity
    # =====================================================

    camera_id: str

    name: str

    source: Any

    # =====================================================
    # Configuration
    # =====================================================

    location: str = "Unknown"

    enabled: bool = True

    stream_type: str = "webcam"
    # webcam | rtsp | video | ip

    resolution: str = "1280x720"

    fps_limit: int = 30

    # =====================================================
    # Runtime State
    # =====================================================

    connected: bool = False

    active: bool = False

    last_frame_time: Optional[datetime] = None

    connected_at: Optional[datetime] = None

    disconnected_at: Optional[datetime] = None

    # =====================================================
    # Statistics
    # =====================================================

    current_fps: float = 0.0

    people_count: int = 0

    congestion_score: float = 0.0

    risk_score: float = 0.0

    uptime_seconds: float = 0.0

    dropped_frames: int = 0

    total_frames: int = 0

    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    # =====================================================
    # Runtime Helpers
    # =====================================================

    def connect(self):

        self.connected = True
        self.active = True
        self.connected_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def disconnect(self):

        self.connected = False
        self.active = False
        self.disconnected_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_statistics(

        self,

        fps: float | None = None,

        people: int | None = None,

        congestion: float | None = None,

        risk: float | None = None

    ):

        if fps is not None:
            self.current_fps = fps

        if people is not None:
            self.people_count = people

        if congestion is not None:
            self.congestion_score = congestion

        if risk is not None:
            self.risk_score = risk

        self.updated_at = datetime.utcnow()

    def frame_received(self):

        self.total_frames += 1
        self.last_frame_time = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def frame_dropped(self):

        self.dropped_frames += 1
        self.updated_at = datetime.utcnow()

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self) -> Dict[str, Any]:

        return {

            "camera_id": self.camera_id,
            "name": self.name,
            "source": self.source,
            "location": self.location,

            "enabled": self.enabled,
            "stream_type": self.stream_type,
            "resolution": self.resolution,
            "fps_limit": self.fps_limit,

            "connected": self.connected,
            "active": self.active,

            "current_fps": self.current_fps,
            "people_count": self.people_count,
            "congestion_score": self.congestion_score,
            "risk_score": self.risk_score,

            "uptime_seconds": self.uptime_seconds,
            "dropped_frames": self.dropped_frames,
            "total_frames": self.total_frames,

            "metadata": self.metadata,

            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),

            "connected_at":
                self.connected_at.isoformat()
                if self.connected_at else None,

            "disconnected_at":
                self.disconnected_at.isoformat()
                if self.disconnected_at else None,

            "last_frame_time":
                self.last_frame_time.isoformat()
                if self.last_frame_time else None
        }

    @classmethod
    def from_dict(

        cls,

        data: Dict[str, Any]

    ) -> "Camera":

        camera = cls(

            camera_id=data["camera_id"],

            name=data["name"],

            source=data["source"],

            location=data.get("location", "Unknown"),

            enabled=data.get("enabled", True),

            stream_type=data.get("stream_type", "webcam"),

            resolution=data.get("resolution", "1280x720"),

            fps_limit=data.get("fps_limit", 30)

        )

        camera.connected = data.get("connected", False)
        camera.active = data.get("active", False)

        camera.current_fps = data.get("current_fps", 0.0)
        camera.people_count = data.get("people_count", 0)
        camera.congestion_score = data.get("congestion_score", 0.0)
        camera.risk_score = data.get("risk_score", 0.0)

        camera.uptime_seconds = data.get("uptime_seconds", 0.0)
        camera.dropped_frames = data.get("dropped_frames", 0)
        camera.total_frames = data.get("total_frames", 0)

        camera.metadata = data.get("metadata", {})

        return camera

    # =====================================================
    # Display
    # =====================================================

    def __str__(self):

        return (

            f"<Camera "

            f"{self.camera_id} "

            f"({self.name}) "

            f"Connected={self.connected} "

            f"People={self.people_count}>"

        )