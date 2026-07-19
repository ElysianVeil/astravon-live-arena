"""
============================================================
Astravon Live Arena
Stream Manager

Purpose:
    Centralized live stream manager responsible for
    encoded frames, streaming queues and subscribers.

Responsibilities:
    • Store latest frame per camera
    • Maintain frame history
    • Manage subscribers
    • Broadcast frames
    • Track streaming metrics
    • Thread-safe operations

Author:
    House of Astravon

Version:
    2.0.0
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from threading import Lock
from datetime import datetime
from typing import Dict, List, Optional, Set

from utils.logger import get_logger

logger = get_logger("StreamManager")


# ============================================================
# Stream State
# ============================================================

@dataclass
class StreamState:

    camera_id: str

    latest_frame: Optional[bytes] = None

    timestamp: datetime = field(default_factory=datetime.utcnow)

    frame_queue: deque = field(
        default_factory=lambda: deque(maxlen=30)
    )

    subscribers: Set[str] = field(default_factory=set)

    frames_sent: int = 0

    bytes_sent: int = 0

    dropped_frames: int = 0

    fps: float = 0.0

    active: bool = True


# ============================================================
# Stream Manager
# ============================================================

class StreamManager:

    def __init__(self):

        self._streams: Dict[str, StreamState] = {}

        self._lock = Lock()

        logger.info("Stream Manager initialized.")

    # --------------------------------------------------------
    # Create Stream
    # --------------------------------------------------------

    def create_stream(
        self,
        camera_id: str
    ) -> StreamState:

        with self._lock:

            if camera_id in self._streams:

                return self._streams[camera_id]

            stream = StreamState(camera_id=camera_id)

            self._streams[camera_id] = stream

            logger.info(
                f"Created stream: {camera_id}"
            )

            return stream

    # --------------------------------------------------------
    # Remove Stream
    # --------------------------------------------------------

    def remove_stream(
        self,
        camera_id: str
    ):

        with self._lock:

            if camera_id in self._streams:

                del self._streams[camera_id]

                logger.info(
                    f"Removed stream: {camera_id}"
                )

    # --------------------------------------------------------
    # Update Frame
    # --------------------------------------------------------

    def update_frame(
        self,
        camera_id: str,
        frame: bytes
    ):

        stream = self.get(camera_id)

        if stream is None:

            stream = self.create_stream(camera_id)

        with self._lock:

            stream.latest_frame = frame

            stream.timestamp = datetime.utcnow()

            stream.frame_queue.append(frame)

    # --------------------------------------------------------
    # Latest Frame
    # --------------------------------------------------------

    def latest_frame(
        self,
        camera_id: str
    ) -> Optional[bytes]:

        stream = self.get(camera_id)

        if stream is None:

            return None

        return stream.latest_frame

    # --------------------------------------------------------
    # Queue
    # --------------------------------------------------------

    def queue(
        self,
        camera_id: str
    ) -> List[bytes]:

        stream = self.get(camera_id)

        if stream is None:

            return []

        return list(stream.frame_queue)

    # --------------------------------------------------------
    # Subscribers
    # --------------------------------------------------------

    def subscribe(
        self,
        camera_id: str,
        client_id: str
    ):

        stream = self.get(camera_id)

        if stream is None:

            stream = self.create_stream(camera_id)

        with self._lock:

            stream.subscribers.add(client_id)

    def unsubscribe(
        self,
        camera_id: str,
        client_id: str
    ):

        stream = self.get(camera_id)

        if stream is None:

            return

        with self._lock:

            stream.subscribers.discard(client_id)

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    def frame_sent(
        self,
        camera_id: str,
        size_bytes: int
    ):

        stream = self.get(camera_id)

        if stream is None:

            return

        with self._lock:

            stream.frames_sent += 1

            stream.bytes_sent += size_bytes

    def dropped_frame(
        self,
        camera_id: str
    ):

        stream = self.get(camera_id)

        if stream is None:

            return

        with self._lock:

            stream.dropped_frames += 1

    def update_fps(
        self,
        camera_id: str,
        fps: float
    ):

        stream = self.get(camera_id)

        if stream is None:

            return

        with self._lock:

            stream.fps = fps

    # --------------------------------------------------------
    # Get Stream
    # --------------------------------------------------------

    def get(
        self,
        camera_id: str
    ) -> Optional[StreamState]:

        return self._streams.get(camera_id)

    # --------------------------------------------------------
    # Broadcast List
    # --------------------------------------------------------

    def subscribers(
        self,
        camera_id: str
    ) -> List[str]:

        stream = self.get(camera_id)

        if stream is None:

            return []

        return list(stream.subscribers)

    # --------------------------------------------------------
    # Snapshot
    # --------------------------------------------------------

    def snapshot(self):

        snapshot = {}

        for camera_id, stream in self._streams.items():

            snapshot[camera_id] = {

                "active": stream.active,

                "subscribers": len(stream.subscribers),

                "frames_sent": stream.frames_sent,

                "bytes_sent": stream.bytes_sent,

                "dropped_frames": stream.dropped_frames,

                "fps": stream.fps,

                "last_update": stream.timestamp.isoformat()

            }

        return snapshot

    # --------------------------------------------------------
    # Count
    # --------------------------------------------------------

    @property
    def stream_count(self):

        return len(self._streams)

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(self):

        with self._lock:

            self._streams.clear()

            logger.info("Stream Manager reset.")