"""
============================================================
Astravon Live Arena
Video Stream

Purpose:
    Continuously reads frames from a camera source.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import threading
import time
from typing import Optional

import cv2

from .camera import Camera

from config import settings
from constants import STREAM_RECONNECT_DELAY
from utils.logger import get_logger
from utils.validators import validate_frame


# ============================================================
# Stream
# ============================================================

logger = get_logger("VideoStream")

class VideoStream:
    """
    Reads frames continuously from a Camera object.

    Runs in a background thread to keep the latest frame
    available without blocking the AI pipeline.
    """

    def __init__(
        self,
        camera: Camera,
        fps_limit: int = settings.FPS
    ) -> None:

        self.camera = camera
        self.fps_limit = fps_limit

        self.frame = None
        self.frame_count = 0
        self.failed_reads = 0
        self.running = False
        self.start_time = None

        self.last_frame_time = None

        self.actual_fps = 0.0

        self.read_time = 0.0

        self.total_read_time = 0.0

        self.max_read_time = 0.0

        self.min_read_time = float("inf")

        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    # ========================================================
    # Control
    # ========================================================

    def start(self) -> None:
        """
        Starts the streaming thread.
        """
        logger.info("Video stream started.")

        if self.running:
            return

        if not self.camera.is_connected():

            if self.camera.reconnect():

                logger.info("Camera reconnected.")

            else:

                logger.error("Reconnect failed.")

                time.sleep(STREAM_RECONNECT_DELAY)

        self.running = True
        self.start_time = time.perf_counter()

        self._thread = threading.Thread(
            target=self._update,
            daemon=True
        )

        self._thread.start()

    def stop(self) -> None:
        """
        Stops the streaming thread.
        """
        logger.info("Video stream stopped.")

        self.running = False

        if self._thread is not None:
            self._thread.join(timeout=1)

    # ========================================================
    # Internal Loop
    # ========================================================

    def _update(self) -> None:
        """
        Continuously reads frames.
        """

        delay = 0

        if self.fps_limit and self.fps_limit > 0:
            delay = 1 / self.fps_limit

        while self.running:

            read_start = time.perf_counter()

            success, frame = self.camera.read()

            elapsed = time.perf_counter() - read_start

            self.read_time = elapsed

            self.total_read_time += elapsed

            self.max_read_time = max(self.max_read_time, elapsed)

            self.min_read_time = min(self.min_read_time, elapsed)

            if not success or not validate_frame(frame):

                self.failed_reads += 1

                if self.failed_reads >= 30:

                    logger.warning("Camera appears disconnected.")

                    self.camera.reconnect()

                    self.failed_reads = 0

                time.sleep(0.05)
                continue

            self.failed_reads = 0

            with self._lock:
                self.frame = frame
                self.frame_count += 1

                self.last_frame_time = time.perf_counter()
                self.frame_timestamp = time.time()

                elapsed_runtime = self.last_frame_time - self.start_time

                if elapsed_runtime > 0:

                    self.actual_fps = self.frame_count / elapsed_runtime

            if delay:
                time.sleep(delay)

    def frame_age(self):

        if self.frame_timestamp is None:

            return None

        return time.time() - self.frame_timestamp
    
    @property
    def average_read_time(self):

        if self.frame_count == 0:

            return 0

        return self.total_read_time / self.frame_count
    
    @property
    def health(self):

        if not self.running:

            return "Stopped"

        if self.failed_reads > 10:

            return "Degraded"

        return "Healthy"
    

    # ========================================================
    # Access
    # ========================================================

    def get_frame(self):
        """
        Returns the latest frame.
        """

        with self._lock:

            if self.frame is None:
                return None

            return self.frame.copy()

    def has_frame(self) -> bool:
        """
        Returns True if at least one frame
        has been captured.
        """

        return self.frame is not None

    # ========================================================
    # Display
    # ========================================================

    def show(
        self,
        window_name: str = "Astravon Camera"
    ) -> None:
        """
        Displays the live stream.
        """

        while self.running:

            frame = self.get_frame()

            if frame is None:
                continue

            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyWindow(window_name)

    # ========================================================
    # Cleanup
    # ========================================================

    def wait_for_frame(self, timeout=5):

        start = time.time()

        while not self.has_frame():

            if time.time() - start > timeout:

                return None

            time.sleep(0.01)

        return self.get_frame()

    def close(self) -> None:
        """
        Stops the stream and closes the camera.
        """

        self.stop()
        self.camera.release()

    def info(self):

        return {

            "running": self.running,

            "health": self.health,

            "camera": self.camera.info(),

            "fps_limit": self.fps_limit,

            "actual_fps": round(self.actual_fps, 2),

            "frames": self.frame_count,

            "failed_reads": self.failed_reads,

            "average_read_time_ms": round(
                self.average_read_time * 1000,
                2
            ),

            "last_frame_age": self.frame_age(),

            "has_frame": self.has_frame()

        }
    
