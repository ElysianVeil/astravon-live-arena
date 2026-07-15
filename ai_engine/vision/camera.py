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

        # --------------------------------------------------------
        # Camera Properties
        # --------------------------------------------------------

        self.width = settings.FRAME_WIDTH
        self.height = settings.FRAME_HEIGHT
        self.fps = settings.FPS

        # --------------------------------------------------------
        # Weather
        # --------------------------------------------------------

        self.weather = None

        # --------------------------------------------------------
        # OpenCV
        # --------------------------------------------------------

        self.capture = None

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
        
        time.sleep(1)

        success = False

        for _ in range(20):

            success, frame = self.capture.read()

            if success and frame is not None:
                break

            time.sleep(0.1)

        if not success:

            logger.error("Camera opened but produced no frames.")

            self.capture.release()

            return False

        self.connected = True

        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            settings.FRAME_WIDTH
        )

        logger.info(
            f"Width={self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)}"
        )

        logger.info(
            f"Height={self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}"
        )

        logger.info(
            f"FPS={self.capture.get(cv2.CAP_PROP_FPS)}"
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            settings.FRAME_HEIGHT
        )

        logger.info(
            f"Width={self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)}"
        )

        logger.info(
            f"Height={self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}"
        )

        logger.info(
            f"FPS={self.capture.get(cv2.CAP_PROP_FPS)}"
        )

        self.capture.set(
            cv2.CAP_PROP_FPS,
            settings.FPS
        )

        logger.info(
            f"Width={self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)}"
        )

        logger.info(
            f"Height={self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}"
        )

        logger.info(
            f"FPS={self.capture.get(cv2.CAP_PROP_FPS)}"
        )

        self.connected = True

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

    def read(self) -> Tuple[bool, Optional[NDArray[np.uint8]]]:
        """
        Reads one frame.

        Returns
        -------
        success, frame
        """

        if self.capture is None:
            return False, None

        success, frame = self.capture.read()

        if not success:
            logger.warning(
                f"No frame received from {self.name}"
            )

        return success, frame

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
                settings.FRAME_WIDTH,
                settings.FRAME_HEIGHT
            ),

            "fps": settings.FPS

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

        self.release()

        return self.connect()