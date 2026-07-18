"""
============================================================
Astravon Live Arena
Camera

Purpose:
    Represents a single camera source and provides
    frame capture functionality.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Optional, Tuple, Union

import requests
import cv2
import uuid
import numpy as np
from numpy.typing import NDArray
import time

from config import settings
from constants import (
    CAMERA_CONNECTED,
    CAMERA_DISCONNECTED,
)
from utils.helpers import current_timestamp
from utils.logger import get_logger
from utils.validators import validate_camera_source


# ============================================================
# Logger
# ============================================================

logger = get_logger("Camera")


# ============================================================
# Camera
# ============================================================

class Camera:
    """
    Represents one camera source.
    """

    def __init__(
        self,
        source: Union[int, str] = settings.DEFAULT_CAMERA,
        name: str = "Camera"
    ):
        """
        Parameters
        ----------
        source:
            Camera index, video file, HTTP stream,
            or RTSP URL.

        name:
            Friendly camera name.
        """

        # --------------------------------------------------------
        # Camera Identity
        # --------------------------------------------------------

        self.id = str(uuid.uuid4())

        # --------------------------------------------------------
        # Global Camera Identity
        # --------------------------------------------------------

        self.global_id = self.id

        self.zone = "Main Entrance"

        self.position = "North"

        self.orientation = "South"

        self.floor = 1

        self.camera_role = "Monitoring"

        self.priority = 1

        self.name = name

        self.source = source

        self.type = "USB"

        self.manufacturer = "Unknown"

        self.model = "Unknown"

        self.venue = "Main Stadium"

        # --------------------------------------------------------
        # Location
        # --------------------------------------------------------

        self.latitude = 0.0
        self.longitude = 0.0

        self.city = "Unknown"
        self.region = "Unknown"
        self.country = "Unknown"

        # --------------------------------------------------------
        # Status
        # --------------------------------------------------------

        self.connected = False

        self.status = "Offline"

        self.connection_time = None

        self.last_frame_time = None

        self.frame_number = 0

        self.frame_timestamp = None

        self.batch_timestamp = None

        # --------------------------------------------------------
        # Camera Properties
        # --------------------------------------------------------

        self.width = settings.FRAME_WIDTH
        self.height = settings.FRAME_HEIGHT
        self.fps = settings.FPS

        self.supports_reid = True

        self.supports_tracking = True

        self.supports_detection = True

        self.supports_streaming = True

        # --------------------------------------------------------
        # Weather
        # --------------------------------------------------------

        self.weather = None

        # --------------------------------------------------------
        # Calibration
        # --------------------------------------------------------

        self.homography = None

        self.calibrated = False

        self.pixel_scale = 1.0

        self.field_of_view = 90.0

        # --------------------------------------------------------
        # OpenCV
        # --------------------------------------------------------

        self.capture = None

        self.frames_read = 0
        self.frames_dropped = 0
        self.read_failures = 0
        self.start_time = None
        self.actual_fps = 0.0
        self.last_frame = None

        self.average_latency = 0.0

        self.maximum_latency = 0.0

        self.minimum_latency = float("inf")

        self.total_latency = 0.0

        # --------------------------------------------------------
        # Health
        # --------------------------------------------------------

        self.health = "Offline"
        self.codec = "Unknown"
        self.backend = "Unknown"
        self.brightness = 0.0
        self.contrast = 0.0
        self.saturation = 0.0
        self.gain = 0.0
        self.exposure = 0.0

        self.status_message = "Offline"
        
        self.error_message = ""

        self.last_error = None

        self.reconnection_attempts = 0

    # ========================================================
    # Connect
    # ========================================================

    def connect(self) -> bool:
        """
        Opens the camera.

        Returns
        -------
        bool
            True if successful.
        """
        if not validate_camera_source(self.source):
            logger.error("Invalid camera source.")
            return False

        logger.info(
            f"Connecting to {self.name} ({self.source})..."
        )

        self.capture = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)

        if not self.capture.isOpened():

            logger.error(
                f"Failed to connect to {self.name}"
            )

            return False
        
        # Warm up camera

        success = False

        for _ in range(30):

            success, frame = self.capture.read()

            if success and frame is not None:

                break

        if not success:

            logger.error("Camera opened but produced no frames.")

            self.capture.release()

            return False


        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            settings.FRAME_WIDTH
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            settings.FRAME_HEIGHT
        )

        self.capture.set(
            cv2.CAP_PROP_FPS,
            settings.FPS
        )

        self.width = int(
            self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        self.height = int(
            self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        self.fps = float(
            self.capture.get(cv2.CAP_PROP_FPS)
        )

        self.backend = self.capture.getBackendName()

        self.brightness = self.capture.get(
            cv2.CAP_PROP_BRIGHTNESS
        )

        self.contrast = self.capture.get(
            cv2.CAP_PROP_CONTRAST
        )

        self.saturation = self.capture.get(
            cv2.CAP_PROP_SATURATION
        )

        self.gain = self.capture.get(
            cv2.CAP_PROP_GAIN
        )

        self.exposure = self.capture.get(
            cv2.CAP_PROP_EXPOSURE
        )

        logger.info(
            f"Resolution: {self.width}x{self.height}"
        )

        logger.info(
            f"FPS: {self.fps:.2f}"
        )

        logger.info(
            f"Backend: {self.backend}"
        )

        self.connected = True

        self.start_time = time.time()

        self.frames_read = 0

        self.read_failures = 0

        self.frames_dropped = 0

        self.health = "Healthy"

        self.connection_time = current_timestamp()

        self.detect_location()

        logger.info(
            f"{CAMERA_CONNECTED}: {self.name}"
        )

        logger.info(
            f"{self.name} connected successfully."
        )

        return True

    # ========================================================
    # Read Frame
    # ========================================================

    def read(self):
        """
        Reads one frame.

        Returns
        -------
        success, frame
        """

        if self.capture is None:

            return False, None

        success, frame = self.capture.read()

        capture_start = time.perf_counter()

        if not success:

            self.read_failures += 1

            self.frames_dropped += 1

            logger.warning(
                f"No frame received from {self.name}"
            )

            if self.read_failures >= 5:

                logger.warning(
                    "Too many failures. Reconnecting..."
                )

                self.reconnect()

            return False, None

        self.frames_read += 1

        self.read_failures = 0

        self.last_frame = frame.copy()

        self.last_frame_time = time.time()

        self.frame_number += 1

        self.frame_timestamp = current_timestamp()

        latency = time.perf_counter() - capture_start

        self.total_latency += latency

        self.maximum_latency = max(

            self.maximum_latency,

            latency

        )

        self.minimum_latency = min(

            self.minimum_latency,

            latency

        )

        self.average_latency = (

            self.total_latency /

            self.frames_read

        )

        elapsed = self.last_frame_time - self.start_time

        if elapsed > 0:

            self.actual_fps = self.frames_read / elapsed

        return True, frame
    
    def frame_packet(self):

        frame = self.get_latest_frame()

        if frame is None:

            return None

        return {

            "camera_id": self.id,

            "global_camera_id": self.global_id,

            "camera_name": self.name,

            "zone": self.zone,

            "position": self.position,

            "orientation": self.orientation,

            "frame_number": self.frame_number,

            "timestamp": self.frame_timestamp,

            "frame": frame,

            "resolution": (

                self.width,

                self.height

            )

        }
    
    def health_report(self):

        return {

            "camera": self.name,

            "status": self.health,

            "fps": round(self.actual_fps,2),

            "latency": round(

                self.average_latency*1000,

                2

            ),

            "frames": self.frames_read,

            "dropped": self.frames_dropped,

            "failures": self.read_failures,

            "reconnections": self.reconnection_attempts

        }

    def get_latest_frame(self):

        """
        Returns the latest successfully captured frame.

        Returns
        -------
        ndarray | None
        """

        if self.last_frame is None:

            return None

        return self.last_frame.copy()
    
    # ========================================================
    # Release
    # ========================================================

    def release(self):
        """
        Releases the camera.
        """

        if self.capture is not None:

            self.capture.release()

            self.capture = None

        self.connected = False

        self.health = "Offline"

        self.last_frame = None

        self.actual_fps = 0.0

        logger.info(
            f"{CAMERA_DISCONNECTED}: {self.name}"
        )

        logger.info(
            f"{self.name} released."
        )

    def detect_location(self):
        """
        Detect the current machine's approximate location
        using IP geolocation.
        """

        try:

            response = requests.get(
                "https://ipapi.co/json/",
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            self.latitude = float(data["latitude"])
            self.longitude = float(data["longitude"])

            self.city = data.get("city")
            self.region = data.get("region")
            self.country = data.get("country_name")

            logger.info(
                f"Detected location: "
                f"{self.city}, "
                f"{self.country} "
                f"({self.latitude}, {self.longitude})"
            )

        except Exception as error:

            logger.warning(
                f"Unable to determine location: {error}"
            )

            self.latitude = 0.0
            self.longitude = 0.0

            self.city = "Unknown"
            self.region = "Unknown"
            self.country = "Unknown"

    # ========================================================
    # Information
    # ========================================================

    def info(self) -> dict:
        """
        Returns camera information.
        """

        return {

            "id": self.id,

            "name": self.name,

            "source": self.source,

            "venue": self.venue,

            "city": self.city,

            "region": self.region,

            "country": self.country,

            "latitude": self.latitude,

            "longitude": self.longitude,

            "connected": self.connected,

            "resolution": (
                self.width,
                self.height
            ),

            "fps": self.fps,

            "actual_fps": round(
                self.actual_fps,
                2
            ),

            "frames_read": self.frames_read,

            "frames_dropped": self.frames_dropped,

            "health": self.health,

            "backend": self.backend,

            "brightness": self.brightness,

            "contrast": self.contrast,

            "saturation": self.saturation,

            "gain": self.gain,

            "exposure": self.exposure,

            "global_id": self.global_id,

            "zone": self.zone,

            "position": self.position,

            "orientation": self.orientation,

            "camera_role": self.camera_role,

            "frame_number": self.frame_number,

            "frame_timestamp": self.frame_timestamp,

            "supports_reid": self.supports_reid,

            "supports_tracking": self.supports_tracking,

            "supports_detection": self.supports_detection,

            "average_latency": round(

                self.average_latency*1000,

                2

            ),

            "reconnections": self.reconnection_attempts,

            "calibrated": self.calibrated,

            "status_message": self.status_message
        }
    
    def summary(self):

        return {

            "camera": self.name,

            "zone": self.zone,

            "connected": self.connected,

            "fps": round(self.actual_fps,2),

            "latency": round(

                self.average_latency*1000,

                2

            ),

            "health": self.health,

            "frame": self.frame_number

        }

    # ========================================================
    # Context Manager
    # ========================================================

    def __enter__(self):

        self.connect()

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):

        self.release()

    def is_connected(self) -> bool:
        """
        Returns whether the camera is connected.
        """

        return self.connected
    
    def reconnect(self) -> bool:
        """
        Attempts to reconnect the camera.
        """

        logger.info(
            f"Reconnecting {self.name}..."
        )
        self.health = "Reconnecting"

        self.reconnection_attempts += 1
        self.release()
        success = self.connect()

        self.health = (
            "Healthy"
            if success
            else "Offline"
        )

        return success