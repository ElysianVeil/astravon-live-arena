"""
============================================================
Astravon Live Arena
Camera Calibration

Purpose:
    Stores calibration information for each camera and
    provides helper methods for converting image
    coordinates into real-world measurements.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import math


# ============================================================
# Camera Calibration
# ============================================================

@dataclass
class CameraCalibration:
    """
    Represents one calibrated camera.
    """

    camera_id: str

    frame_width: int
    frame_height: int

    # Approximate metres represented by one pixel.
    metres_per_pixel: float = 0.02

    # Camera installation height.
    camera_height: float = 3.0

    # Camera viewing angle.
    camera_angle: float = 45.0


# ============================================================
# Calibration Manager
# ============================================================

class CalibrationManager:
    """
    Stores calibration information
    for multiple cameras.
    """

    def __init__(self):

        self.calibrations: Dict[
            str,
            CameraCalibration
        ] = {}

    # ========================================================
    # Register
    # ========================================================

    def register(
        self,
        calibration: CameraCalibration
    ) -> None:
        """
        Register a calibrated camera.
        """

        self.calibrations[
            calibration.camera_id
        ] = calibration

    # ========================================================
    # Retrieve
    # ========================================================

    def get(
        self,
        camera_id: str
    ) -> Optional[CameraCalibration]:
        """
        Returns calibration information.
        """

        return self.calibrations.get(camera_id)

    # ========================================================
    # Pixel Distance
    # ========================================================

    @staticmethod
    def pixel_distance(
        point_a: Tuple[int, int],
        point_b: Tuple[int, int]
    ) -> float:
        """
        Returns Euclidean distance in pixels.
        """

        return math.dist(point_a, point_b)

    # ========================================================
    # Metres
    # ========================================================

    def metres_between(
        self,
        camera_id: str,
        point_a: Tuple[int, int],
        point_b: Tuple[int, int]
    ) -> Optional[float]:
        """
        Converts pixel distance into metres.
        """

        calibration = self.get(camera_id)

        if calibration is None:
            return None

        pixels = self.pixel_distance(
            point_a,
            point_b
        )

        return (
            pixels *
            calibration.metres_per_pixel
        )

    # ========================================================
    # Bounding Box Centre
    # ========================================================

    @staticmethod
    def centre(
        bbox: List[int]
    ) -> Tuple[int, int]:
        """
        Returns the centre of a bounding box.
        """

        x1, y1, x2, y2 = bbox

        return (
            (x1 + x2) // 2,
            (y1 + y2) // 2
        )

    # ========================================================
    # Bottom Centre
    # ========================================================

    @staticmethod
    def foot_position(
        bbox: List[int]
    ) -> Tuple[int, int]:
        """
        Returns the bottom centre of a person.

        This approximates where the person's
        feet touch the ground.
        """

        x1, y1, x2, y2 = bbox

        return (
            (x1 + x2) // 2,
            y2
        )

    # ========================================================
    # Area
    # ========================================================

    def estimate_area(
        self,
        camera_id: str
    ) -> Optional[float]:
        """
        Estimates visible area in square metres.
        """

        calibration = self.get(camera_id)

        if calibration is None:
            return None

        width = (
            calibration.frame_width *
            calibration.metres_per_pixel
        )

        height = (
            calibration.frame_height *
            calibration.metres_per_pixel
        )

        return width * height