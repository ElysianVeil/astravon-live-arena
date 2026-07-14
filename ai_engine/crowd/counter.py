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

from typing import Dict, List


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
        self.current_count = 0
        self.maximum_count = 0
        self.total_detected = 0

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

        self.current_count = count

        if count > self.maximum_count:
            self.maximum_count = count

        self.total_detected += count

        return count

    # --------------------------------------------------------

    def reset(self):
        """
        Reset all statistics.
        """

        self.current_count = 0
        self.maximum_count = 0
        self.total_detected = 0

    # --------------------------------------------------------

    def statistics(self) -> Dict:
        """
        Returns crowd statistics.
        """

        return {
            "current_count": self.current_count,
            "maximum_count": self.maximum_count,
            "total_detected": self.total_detected,
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

    def average_count(
        self,
        frames_processed: int
    ) -> float:
        """
        Calculates the average crowd count across frames.
        """

        if frames_processed <= 0:
            return 0.0

        return round(
            self.total_detected / frames_processed,
            2
        )


# ============================================================
# Singleton Instance
# ============================================================

crowd_counter = CrowdCounter()