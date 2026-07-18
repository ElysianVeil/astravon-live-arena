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
import time
from collections import deque, defaultdict
from typing import Optional

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

        # Performance
        self.frames_processed = 0
        self.processing_time = 0.0
        self.total_processing_time = 0.0
        self.previous_centers = {}
        self.track_age = defaultdict(int)

        # Statistics
        self.total_tracks_created = 0
        self.max_active_tracks = 0

        # State
        self.last_tracks = []
        self.track_history = defaultdict(lambda: deque(maxlen=50))
        self.last_update_time = None

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

        start = time.perf_counter()

        tracked = self.tracker.update_with_detections(detections)

        elapsed = time.perf_counter() - start

        self.processing_time = elapsed
        self.total_processing_time += elapsed
        self.frames_processed += 1
        self.last_update_time = time.time()

        active_tracks = len(tracked)

        self.max_active_tracks = max(
            self.max_active_tracks,
            active_tracks
        )

        self.total_tracks_created += max(
            0,
            active_tracks - len(self.last_tracks)
        )

        self.last_tracks = tracked

        return tracked

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
            center = (
                int((x1+x2)/2),
                int((y1+y2)/2)
            )
            self.track_history[int(tracker_id)].append(center)
            self.track_age[int(tracker_id)] += 1
            previous = self.previous_centers.get(
                int(tracker_id)
            )

            velocity = (0, 0)

            if previous:

                velocity = (

                    center[0] - previous[0],

                    center[1] - previous[1]

                )

            self.previous_centers[int(tracker_id)] = center

            tracks.append(
                {
                    "track_id": int(tracker_id),
                    "class_id": int(class_id),
                    "confidence": float(confidence),
                    "center": center,
                    "velocity": velocity,
                    "history": list(
                        self.track_history[int(tracker_id)]
                    ),
                    "age": self.track_age[int(tracker_id)],
                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2
                    ]
                }
            )

        return tracks
    
    def get_people(
        self,
        tracks
    ):

        return [

            track

            for track in tracks

            if track["class_id"] == PERSON_CLASS_ID

        ]
        
    def get_track(
        self,
        track_id: int
    ) -> Optional[Dict]:

        for track in self.last_tracks:

            if track.tracker_id == track_id:
                return track

        return None
    
    def nearest_track(
        self,
        point
    ):

        nearest = None
        distance = float("inf")

        for track in self.get_tracks(
            self.last_tracks
        ):

            cx, cy = track["center"]

            d = np.hypot(
                point[0] - cx,
                point[1] - cy
            )

            if d < distance:

                distance = d

                nearest = track

        return nearest

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
    
    def active_ids(self):

        ids = []

        for track in self.last_tracks:

            if track.tracker_id is not None:
                ids.append(int(track.tracker_id))

        return ids
    
    def has_track(
        self,
        track_id
    ):

        return track_id in self.active_ids()

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

        self.track_history.clear()

        self.last_tracks = []
    
    @property
    def average_processing_time(self):

        if self.frames_processed == 0:
            return 0.0

        return (

            self.total_processing_time

            /

            self.frames_processed

        )
    
    @property
    def fps(self):

        if self.processing_time == 0:
            return 0

        return 1 / self.processing_time

    def info(self) -> dict:
        return {

            "tracker": "ByteTrack",

            "configured_fps": settings.FPS,

            "frames_processed":
                self.frames_processed,

            "active_tracks":
                len(self.last_tracks),

            "maximum_active_tracks":
                self.max_active_tracks,

            "total_tracks_created":
                self.total_tracks_created,

            "processing_time_ms":
                round(
                    self.processing_time * 1000,
                    2
                ),

            "average_processing_time_ms":
                round(
                    self.average_processing_time * 1000,
                    2
                ),

            "tracking_fps":
                round(
                    self.fps,
                    2
                ),

            "last_update":
                self.last_update_time

        }