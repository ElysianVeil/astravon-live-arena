"""
============================================================
Astravon Live Arena
Crowd Movement Analyzer

Purpose:
    Tracks the movement of people between frames
    and calculates movement statistics.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from math import sqrt
from typing import Dict, List, Tuple


# ============================================================
# Movement Analyzer
# ============================================================

class MovementAnalyzer:
    """
    Analyzes crowd movement using tracked IDs.
    """

    def __init__(self):
        self.previous_positions: Dict[int, Tuple[int, int]] = {}

    # --------------------------------------------------------

    @staticmethod
    def _distance(
        point1: Tuple[int, int],
        point2: Tuple[int, int]
    ) -> float:
        """
        Calculates Euclidean distance.
        """

        return sqrt(
            (point2[0] - point1[0]) ** 2 +
            (point2[1] - point1[1]) ** 2
        )

    # --------------------------------------------------------

    def analyze(
        self,
        tracked_objects: List[Dict]
    ) -> Dict:
        """
        Calculates movement statistics.

        Expected object format:

        {
            "track_id": 7,
            "center": (x, y)
        }
        """

        movement_distances = []

        stationary = 0
        moving = 0

        for obj in tracked_objects:

            track_id = obj.get("track_id")
            center = obj.get("center")

            if track_id is None or center is None:
                continue

            if track_id in self.previous_positions:

                distance = self._distance(
                    self.previous_positions[track_id],
                    center
                )

                movement_distances.append(distance)

                if distance < 5:
                    stationary += 1
                else:
                    moving += 1

            self.previous_positions[track_id] = center

        average_speed = (
            sum(movement_distances) / len(movement_distances)
            if movement_distances
            else 0.0
        )

        return {
            "tracked_people": len(tracked_objects),
            "moving_people": moving,
            "stationary_people": stationary,
            "average_movement": round(
                average_speed,
                2
            )
        }

    # --------------------------------------------------------

    def clear(self):
        """
        Clears stored movement history.
        """

        self.previous_positions.clear()

    # --------------------------------------------------------

    def tracked_count(self) -> int:
        """
        Returns number of tracked people.
        """

        return len(self.previous_positions)


# ============================================================
# Singleton
# ============================================================

movement_analyzer = MovementAnalyzer()