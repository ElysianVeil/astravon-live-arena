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

            if not self.camera.connect():

                logger.error(
                    "Unable to start stream."
                )

                return

        self.running = True

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

            success, frame = self.camera.read()

            if not success:

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

            if delay:
                time.sleep(delay)

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

    def close(self) -> None:
        """
        Stops the stream and closes the camera.
        """

        self.stop()
        self.camera.release()

    def info(self):

        return {

            "running": self.running,

            "camera": self.camera.info(),

            "fps_limit": self.fps_limit,

            "has_frame": self.has_frame()
        }
    
