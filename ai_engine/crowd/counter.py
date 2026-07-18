"""
============================================================
Astravon Live Arena
Crowd Counter

Purpose:
    Counts people detected by the AI engine and provides
    basic crowd statistics.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import time
from collections import deque
from statistics import mean
from typing import Deque, Dict, List, Set

from constants import PERSON_CLASS_ID
from utils.logger import get_logger
from config import settings

logger = get_logger("CrowdCounter")


# ============================================================
# Crowd Counter
# ============================================================

class CrowdCounter:
    """
    Handles crowd counting operations.

    Expected detection format:

    {
        "track_id": 1,
        "class_name": "person",
        "confidence": 0.94,
        "bbox": (x1, y1, x2, y2),
        "center": (cx, cy)
    }
    """

    def __init__(self):

        # Current frame
        self.current_count = 0

        # Highest simultaneous count
        self.maximum_count = 0

        # Sum across all processed frames
        self.total_detected = 0

        # Number of processed frames
        self.frames_processed = 0

        # Unique people seen
        self.unique_people: Set[int] = set()

        # IDs currently visible
        self.active_tracks: Set[int] = set()

        # Crowd history
        self.history: Deque[int] = deque(maxlen=500)

        # Entry / Exit counters
        self.entries = 0
        self.exits = 0

        # Previous frame IDs
        self.previous_tracks: Set[int] = set()

        # Timing
        self.start_time = time.time()
    # --------------------------------------------------------

    def count_people(
        self,
        tracks: List[Dict]
    ) -> int:
        """
        Counts the number of people in the current frame.
        """

        count = sum(
            1
            for track in tracks
            if track.get("class_id") == 0
        )

        self.frames_processed += 1

        self.total_detected += count

        self.history.append(count)

        current_tracks = {

            track["track_id"]

            for track in tracks

            if track["class_id"] == PERSON_CLASS_ID

        }

        self.unique_people.update(current_tracks)

        entered = current_tracks - self.previous_tracks

        self.entries += len(entered)

        left = self.previous_tracks - current_tracks

        self.exits += len(left)

        self.previous_tracks = current_tracks

        self.active_tracks = current_tracks

        self.current_count = count

        if count > self.maximum_count:
            self.maximum_count = count

        self.total_detected += count

        logger.debug(

            f"People={self.current_count} | "

            f"Entries={self.entries} | "

            f"Exits={self.exits} | "

            f"Peak={self.maximum_count}"

        )

        return count

    # --------------------------------------------------------

    def reset(self):
        """
        Reset all statistics.
        """

        self.current_count = 0
        self.maximum_count = 0
        self.total_detected = 0
        self.frames_processed = 0

        self.unique_people.clear()

        self.previous_tracks.clear()

        self.active_tracks.clear()

        self.entries = 0

        self.exits = 0

        self.history.clear()

        self.start_time = time.time()

    # --------------------------------------------------------

    def statistics(self) -> Dict:
        """
        Returns crowd statistics.
        """

        return {

            "current_count": self.current_count,

            "peak_count": self.maximum_count,

            "average_count": self.average_count(),

            "rolling_average": self.rolling_average(),

            "occupancy": self.occupancy(),

            "crowd_level": self.level(),

            "entries": self.entries,

            "exits": self.exits,

            "unique_people": len(self.unique_people),

            "active_tracks": len(self.active_tracks),

            "frames_processed": self.frames_processed,

            "people_per_minute": self.people_per_minute(),

            "trend": self.trend(),

            "uptime": self.uptime

        }
    # --------------------------------------------------------

    def has_people(self) -> bool:
        """
        Returns True if at least one person is present.
        """

        return self.current_count > 0

    # --------------------------------------------------------

    def is_empty(self) -> bool:
        """
        Returns True if the monitored area is empty.
        """

        return self.current_count == 0

    # --------------------------------------------------------

    def get_current_count(self) -> int:
        """
        Returns the current crowd count.
        """

        return self.current_count

    # --------------------------------------------------------

    def get_peak_count(self) -> int:
        """
        Returns the highest crowd count observed.
        """

        return self.maximum_count

    # --------------------------------------------------------

    def average_count(self):

        if self.frames_processed == 0:
            return 0

        return round(

            self.total_detected /

            self.frames_processed,

            2

        )
    
    def trend(self):

        if len(self.history) < 2:
            return "Stable"

        previous = self.history[-2]
        current = self.history[-1]

        if current > previous:
            return "Increasing"

        if current < previous:
            return "Decreasing"

        return "Stable"
    
    def rolling_average(

        self,

        window=30

    ):

        if not self.history:
            return 0

        values = list(self.history)[-window:]

        return round(

            mean(values),

            2

        )
    
    def occupancy(self):

        return round(

            self.current_count /

            settings.VENUE_CAPACITY * 100,

            2

        )
    
    def level(self):

        occupancy = self.occupancy()

        if occupancy < 25:
            return "Low"

        if occupancy < 50:
            return "Moderate"

        if occupancy < 75:
            return "High"

        return "Critical"
    
    def people_per_minute(self):

        elapsed = (

            time.time()

            -

            self.start_time

        ) / 60

        if elapsed <= 0:
            return 0

        return round(

            self.entries /

            elapsed,

            2

        )
    
    @property
    def uptime(self):

        return round(

            time.time()

            -

            self.start_time,

            2

        )
    
    @property
    def peak(self):
        return self.maximum_count


    @property
    def unique_count(self):
        return len(self.unique_people)


    @property
    def active_count(self):
        return len(self.active_tracks)
    


# ============================================================
# Singleton Instance
# ============================================================

crowd_counter = CrowdCounter()