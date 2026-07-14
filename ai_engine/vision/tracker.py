"""
============================================================
Astravon Live Arena
ByteTrack Tracker

Purpose:
    Tracks detected people across video frames using
    ByteTrack.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Dict, List

import numpy as np
from supervision import ByteTrack

from config import settings
from constants import PERSON_CLASS_ID
from utils.logger import get_logger

# ============================================================
# ByteTrack Wrapper
# ============================================================
logger = get_logger("PersonTracker")

class PersonTracker:
    """
    Wrapper around ByteTrack.

    Responsible for assigning persistent IDs to detected
    people across consecutive frames.
    """

    def __init__(
        self,
        fps: int = settings.FPS
    ) -> None:

        logger.info("ByteTrack initialized.")

        self.tracker = ByteTrack(
            frame_rate=fps
        )

    # ========================================================
    # Tracking
    # ========================================================

    def update(
        self,
        detections
    ):
        """
        Updates the tracker.

        Args:
            detections:
                supervision.Detections object.

        Returns:
            Tracked detections.
        """

        return self.tracker.update_with_detections(
            detections
        )

    # ========================================================
    # Extract Track Information
    # ========================================================

    def get_tracks(
        self,
        tracked
    ) -> List[Dict]:
        """
        Converts tracked detections into dictionaries.
        """

        tracks = []

        if len(tracked) == 0:
            return tracks

        for bbox, confidence, class_id, tracker_id in zip(
            tracked.xyxy,
            tracked.confidence,
            tracked.class_id,
            tracked.tracker_id
        ):

            x1, y1, x2, y2 = bbox.astype(int)

            tracks.append(
                {
                    "track_id": int(tracker_id),
                    "class_id": int(class_id),
                    "confidence": float(confidence),
                    "center": (
                        int((x1 + x2) / 2),
                        int((y1 + y2) / 2),
                    ),
                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2
                    ]
                }
            )

        return tracks

    # ========================================================
    # Count Active Tracks
    # ========================================================

    def count(
        self,
        tracked
    ) -> int:
        """
        Returns active tracked objects.
        """

        return len(tracked)

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Clears tracker memory.

        Useful when switching cameras.
        """
        logger.info("Tracker reset.")

        self.tracker.reset()

    def info(self) -> dict:
        return {
            "fps": settings.FPS,
            "tracker": "ByteTrack",
        }