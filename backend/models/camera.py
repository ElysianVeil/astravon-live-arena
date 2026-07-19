"""
============================================================
Astravon Live Arena
Camera Model

Purpose:
    Database model representing registered cameras
    connected to the Astravon Live Arena system.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    JSON,
    String,
    Text
)

from database.base import Base


class Camera(Base):
    """
    Stores registered cameras.

    Live frame data is NOT stored here.
    This table stores camera configuration
    and its latest known state.
    """

    __tablename__ = "cameras"

    # ========================================================
    # Primary Key
    # ========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ========================================================
    # Camera Identity
    # ========================================================

    camera_id = Column(
        String(64),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(120),
        nullable=False
    )

    location = Column(
        String(120),
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    # ========================================================
    # Camera Source
    # ========================================================

    source = Column(
        String(255),
        nullable=False
    )

    source_type = Column(
        String(30),
        default="webcam"
    )
    # webcam
    # rtsp
    # ip
    # video

    resolution = Column(
        String(30),
        default="1280x720"
    )

    fps_limit = Column(
        Integer,
        default=30
    )

    # ========================================================
    # Runtime Status
    # ========================================================

    enabled = Column(
        Boolean,
        default=True
    )

    connected = Column(
        Boolean,
        default=False
    )

    active = Column(
        Boolean,
        default=False
    )

    recording = Column(
        Boolean,
        default=False
    )

    # ========================================================
    # Latest Statistics
    # ========================================================

    current_fps = Column(
        Float,
        default=0.0
    )

    people_count = Column(
        Integer,
        default=0
    )

    congestion_score = Column(
        Float,
        default=0.0
    )

    risk_score = Column(
        Float,
        default=0.0
    )

    dropped_frames = Column(
        Integer,
        default=0
    )

    total_frames = Column(
        Integer,
        default=0
    )

    # ========================================================
    # Camera Configuration
    # ========================================================

    metadata = Column(
        JSON,
        nullable=True
    )

    # ========================================================
    # Connection Times
    # ========================================================

    last_frame_at = Column(
        DateTime,
        nullable=True
    )

    connected_at = Column(
        DateTime,
        nullable=True
    )

    disconnected_at = Column(
        DateTime,
        nullable=True
    )

    # ========================================================
    # Audit
    # ========================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ========================================================
    # Representation
    # ========================================================

    def __repr__(self):

        return (
            f"<Camera("
            f"id={self.id}, "
            f"camera_id='{self.camera_id}', "
            f"name='{self.name}', "
            f"connected={self.connected}"
            f")>"
        )