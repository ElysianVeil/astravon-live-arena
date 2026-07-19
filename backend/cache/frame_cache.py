"""
============================================================
Astravon Live Arena
Frame Cache

Purpose:
    High-performance in-memory frame cache for live camera
    streaming.

Responsibilities:
    • Store latest encoded frame per camera
    • Keep previous frame
    • Timestamp frames
    • Frame age calculations
    • Thread-safe access
    • Automatic cleanup
    • Cache statistics

Author:
    House of Astravon

Version:
    2.0.0
============================================================
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional

from utils.logger import get_logger

logger = get_logger("FrameCache")


# ============================================================
# Frame Entry
# ============================================================

@dataclass(slots=True)
class FrameEntry:

    camera_id: str

    frame: bytes

    frame_number: int

    timestamp: float

    width: int

    height: int

    fps: float


# ============================================================
# Frame Cache
# ============================================================

class FrameCache:

    def __init__(self):

        self._frames: Dict[str, FrameEntry] = {}

        self._previous_frames: Dict[str, FrameEntry] = {}

        self._lock = threading.RLock()

        self._hits = 0

        self._misses = 0

        logger.info("Frame Cache initialized.")

    # ========================================================
    # Store Frame
    # ========================================================

    def update(
        self,
        camera_id: str,
        frame: bytes,
        frame_number: int,
        width: int,
        height: int,
        fps: float
    ):

        now = time.time()

        with self._lock:

            if camera_id in self._frames:

                self._previous_frames[camera_id] = self._frames[camera_id]

            self._frames[camera_id] = FrameEntry(

                camera_id=camera_id,

                frame=frame,

                frame_number=frame_number,

                timestamp=now,

                width=width,

                height=height,

                fps=fps

            )

    # ========================================================
    # Latest Frame
    # ========================================================

    def get(
        self,
        camera_id: str
    ) -> Optional[FrameEntry]:

        with self._lock:

            frame = self._frames.get(camera_id)

            if frame:

                self._hits += 1

            else:

                self._misses += 1

            return frame

    # ========================================================
    # Previous Frame
    # ========================================================

    def previous(
        self,
        camera_id: str
    ) -> Optional[FrameEntry]:

        with self._lock:

            return self._previous_frames.get(camera_id)

    # ========================================================
    # Frame Exists
    # ========================================================

    def exists(
        self,
        camera_id: str
    ) -> bool:

        with self._lock:

            return camera_id in self._frames

    # ========================================================
    # Remove Camera
    # ========================================================

    def remove(
        self,
        camera_id: str
    ):

        with self._lock:

            self._frames.pop(camera_id, None)

            self._previous_frames.pop(camera_id, None)

    # ========================================================
    # Clear
    # ========================================================

    def clear(self):

        with self._lock:

            self._frames.clear()

            self._previous_frames.clear()

            self._hits = 0

            self._misses = 0

    # ========================================================
    # Cleanup
    # ========================================================

    def cleanup(
        self,
        max_age_seconds: float = 30.0
    ):

        now = time.time()

        with self._lock:

            expired = [

                camera

                for camera, frame

                in self._frames.items()

                if now - frame.timestamp > max_age_seconds

            ]

            for camera in expired:

                self.remove(camera)

        if expired:

            logger.info(

                "Removed %d stale frame(s).",

                len(expired)

            )

    # ========================================================
    # Frame Age
    # ========================================================

    def frame_age(
        self,
        camera_id: str
    ) -> Optional[float]:

        frame = self.get(camera_id)

        if frame is None:

            return None

        return time.time() - frame.timestamp

    # ========================================================
    # Cameras
    # ========================================================

    def cameras(self):

        with self._lock:

            return list(self._frames.keys())

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):

        with self._lock:

            total = self._hits + self._misses

            hit_rate = 0.0

            if total:

                hit_rate = self._hits / total

            return {

                "cached_cameras": len(self._frames),

                "previous_frames": len(self._previous_frames),

                "cache_hits": self._hits,

                "cache_misses": self._misses,

                "hit_rate": round(hit_rate, 3)

            }

    # ========================================================
    # Information
    # ========================================================

    def info(self):

        with self._lock:

            return {

                camera: {

                    "frame": entry.frame_number,

                    "resolution": f"{entry.width}x{entry.height}",

                    "fps": round(entry.fps, 2),

                    "age_seconds": round(

                        time.time() - entry.timestamp,

                        2

                    )

                }

                for camera, entry

                in self._frames.items()

            }

    # ========================================================
    # Length
    # ========================================================

    def __len__(self):

        return len(self._frames)

    # ========================================================
    # Contains
    # ========================================================

    def __contains__(
        self,
        camera_id: str
    ):

        return self.exists(camera_id)