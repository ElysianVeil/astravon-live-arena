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

        if calibration.frame_width <= 0:
            raise ValueError("Frame width must be positive.")

        if calibration.frame_height <= 0:
            raise ValueError("Frame height must be positive.")

        if calibration.metres_per_pixel <= 0:
            raise ValueError("metres_per_pixel must be positive.")

        self.calibrations[calibration.camera_id] = calibration

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

    def update(self, camera_id: str, **kwargs):

        calibration = self.get(camera_id)

        if calibration is None:
            return False

        for key, value in kwargs.items():

            if not hasattr(calibration, key):

                continue

            if key in (
                "frame_width",
                "frame_height",
                "metres_per_pixel"
            ) and value <= 0:

                raise ValueError(
                    f"{key} must be positive."
                )

            setattr(
                calibration,
                key,
                value
            )

        return True
    
    def remove(self, camera_id):

        return self.calibrations.pop(camera_id, None)

    def calibrated(self, camera_id):

        return camera_id in self.calibrations
    
    def export(self):

        return {

            cid: vars(calibration)

            for cid, calibration

            in self.calibrations.items()

        }
    
    def load(
        self,
        data: Dict[str, dict]
    ) -> None:
        """
        Loads calibration data.
        """

        self.calibrations.clear()

        for values in data.values():

            calibration = CameraCalibration(
                **values
            )

            self.register(calibration)
    
    @property
    def count(self):

        return len(self.calibrations)
    
    # ========================================================
    # Information
    # ========================================================

    def info(self) -> dict:
        """
        Returns calibration manager information.
        """

        return {

            "registered": self.count,

            "camera_ids": list(
                self.calibrations.keys()
            )

        }
    
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
    # Pixels to Metres
    # ========================================================

    def pixels_to_metres(
        self,
        camera_id: str,
        pixels: float
    ) -> Optional[float]:
        """
        Converts a pixel distance directly into metres.
        """

        calibration = self.get(camera_id)

        if calibration is None:

            return None

        return pixels * calibration.metres_per_pixel

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

        return self.pixels_to_metres(
            camera_id,
            pixels
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
    # Person Distance
    # ========================================================

    def person_distance(
        self,
        camera_id: str,
        bbox_a: List[int],
        bbox_b: List[int]
    ) -> Optional[float]:
        """
        Estimates the ground distance between two people.
        """

        point_a = self.foot_position(bbox_a)

        point_b = self.foot_position(bbox_b)

        return self.metres_between(
            camera_id,
            point_a,
            point_b
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