"""
============================================================
Astravon Live Arena
Drawing Utilities

Purpose:
    Draws detections, tracked people, statistics,
    zones, and alerts on video frames.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import cv2
import numpy as np

from config import settings
from constants import (
    COLOR_RED,
    COLOR_YELLOW,
    COLOR_ORANGE,
    COLOR_GREEN,
    COLOR_WHITE,
)
from utils.logger import get_logger

# ============================================================
# Drawing
# ============================================================

logger = get_logger("Drawing")

class Drawing:

    # --------------------------------------------------------
    # Bounding Boxes
    # --------------------------------------------------------

    @staticmethod
    def draw_detection(
        frame: np.ndarray,
        bbox: List[int],
        label: str,
        confidence: float,
        color: Tuple[int, int, int] = COLOR_GREEN
    ) -> np.ndarray:
        """
        Draws one detection.
        """

        x1, y1, x2, y2 = bbox

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        text = f"{label} {confidence:.2f}"

        cv2.putText(
            frame,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

        return frame
    
    @staticmethod
    def draw_detections(
        frame,
        detections
    ):

        for detection in detections:

            Drawing.draw_detection(
                frame,
                detection["bbox"],
                detection["class_name"],
                detection["confidence"]
            )

        return frame

    # --------------------------------------------------------
    # Tracks
    # --------------------------------------------------------

    @staticmethod
    def draw_track(
        frame: np.ndarray,
        track: Dict
    ) -> np.ndarray:
        """
        Draws one tracked person.
        """

        x1, y1, x2, y2 = track["bbox"]

        track_id = track["track_id"]

        color = (255, 180, 0)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cv2.putText(
            frame,
            f"Person {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

        return frame

    # --------------------------------------------------------
    # Multiple Tracks
    # --------------------------------------------------------

    @staticmethod
    def draw_tracks(
        frame: np.ndarray,
        tracks: List[Dict]
    ) -> np.ndarray:
        """
        Draws every tracked person.
        """

        for track in tracks:
            Drawing.draw_track(
                frame,
                track
            )

        return frame

    # --------------------------------------------------------
    # Statistics Panel
    # --------------------------------------------------------

    @staticmethod
    def draw_statistics(
        frame: np.ndarray,
        people_count: int,
        density: str,
        occupancy: float,
        temperature: float,
        risk_score: int
    ) -> np.ndarray:
        """
        Draws statistics.
        """

        lines = [
            f"People: {people_count}",
            f"Density: {density}",
            f"Occupancy: {occupancy:.1f}%",
            f"Temperature: {temperature:.1f} C",
            f"Risk Score: {risk_score}"
        ]

        x = 20
        y = 30

        for line in lines:

            cv2.putText(
                frame,
                line,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            y += 30

        return frame

    # --------------------------------------------------------
    # Alert
    # --------------------------------------------------------

    @staticmethod
    def draw_alert(
        frame: np.ndarray,
        title: str,
        severity: str
    ) -> np.ndarray:
        """
        Displays an alert banner.
        """

        color = (0, 255, 255)

        if severity.lower() == "medium":
            color = (0, 165, 255)

        elif severity.lower() == "high":
            color = (0, 0, 255)

        cv2.rectangle(
            frame,
            (0, 0),
            (frame.shape[1], 45),
            color,
            -1
        )

        cv2.putText(
            frame,
            f"{severity.upper()} : {title}",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        return frame

    # --------------------------------------------------------
    # FPS
    # --------------------------------------------------------

    @staticmethod
    def draw_fps(
        frame: np.ndarray,
        fps: float
    ) -> np.ndarray:
        """
        Displays FPS.
        """

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        return frame

    # --------------------------------------------------------
    # Camera Name
    # --------------------------------------------------------

    @staticmethod
    def draw_camera_name(
        frame: np.ndarray,
        camera_name: str
    ) -> np.ndarray:
        """
        Displays the camera name.
        """

        cv2.putText(
            frame,
            camera_name,
            (frame.shape[1] - 220, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        return frame

    # --------------------------------------------------------
    # Crosshair
    # --------------------------------------------------------

    @staticmethod
    def draw_crosshair(
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Draws a centre crosshair.
        """

        h, w = frame.shape[:2]

        cx = w // 2
        cy = h // 2

        cv2.line(
            frame,
            (cx - 20, cy),
            (cx + 20, cy),
            (0, 255, 255),
            2
        )

        cv2.line(
            frame,
            (cx, cy - 20),
            (cx, cy + 20),
            (0, 255, 255),
            2
        )

        return frame