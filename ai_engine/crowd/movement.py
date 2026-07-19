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
import time
from collections import deque


# ============================================================
# Movement Analyzer
# ============================================================

class MovementAnalyzer:
    """
    Analyzes crowd movement using tracked IDs.
    """

    def __init__(self):
        self.previous_positions: Dict[int, Tuple[int, int]] = {}
        self.previous_positions = {}

        self.track_history = {}

        self.total_distance = {}

        self.current_speed = {}

        self.direction = {}

        self.stationary_frames = {}

        self.moving_frames = {}

        self.last_seen = {}

        self.frames_processed = 0

        self.processing_time = 0.0

        self.total_processing_time = 0.0


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
        start = time.perf_counter()

        movement_distances = []

        stationary = 0
        moving = 0
        total_dx = 0
        total_dy = 0
        fastest = None
        max_speed = 0

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

                previous = self.previous_positions[track_id]

                dx = center[0] - previous[0]
                dy = center[1] - previous[1]

                total_dx += dx
                total_dy += dy

                self.direction[track_id] = (dx, dy)

                self.total_distance[track_id] = (

                    self.total_distance.get(track_id, 0)

                    +

                    distance

                )

                self.current_speed[track_id] = distance

                movement_distances.append(distance)

                if distance > max_speed:

                    max_speed = distance
                    fastest = track_id

                if distance < 5:

                    stationary += 1

                    self.stationary_frames[track_id] = (

                        self.stationary_frames.get(track_id, 0)

                        + 1

                    )

                    self.moving_frames[track_id] = 0

                else:

                    moving += 1

                    self.stationary_frames[track_id] = 0

                    self.moving_frames[track_id] = (

                        self.moving_frames.get(track_id, 0)

                        + 1

                    )

            history = self.track_history.setdefault(
                track_id,
                deque(maxlen=30)
            )

            history.append(center)

            self.previous_positions[track_id] = center

        average_speed = (
            sum(movement_distances) / len(movement_distances)
            if movement_distances
            else 0.0
        )

        if average_speed < 2:

            flow = "Still"

        elif average_speed < 8:

            flow = "Walking"

        elif average_speed < 20:

            flow = "Busy"

        else:

            flow = "Running"

        elapsed = time.perf_counter() - start

        self.processing_time = elapsed
        self.total_processing_time += elapsed
        self.frames_processed += 1

        active = {

            obj["track_id"]

            for obj in tracked_objects

        }

        for track_id in list(self.previous_positions):

            if track_id not in active:

                self.previous_positions.pop(track_id,None)

                self.track_history.pop(track_id,None)

                self.total_distance.pop(track_id,None)

                self.current_speed.pop(track_id,None)

                self.direction.pop(track_id,None)

                self.stationary_frames.pop(track_id,None)

                self.moving_frames.pop(track_id,None)

        return {
            "tracked_people": len(tracked_objects),
            "moving_people": moving,
            "stationary_people": stationary,
            "crowd_direction": (
                total_dx,
                total_dy
            ),
            "fastest_track": fastest,
            "flow_level": flow,
            "max_speed": round(
                max_speed,
                2
            ),
            "average_movement": round(
                average_speed,
                2
            )
        }
    
    @property
    def fps(self):

        if self.processing_time == 0:
            return 0

        return 1 / self.processing_time
    
    @property
    def average_processing_time(self):

        if self.frames_processed == 0:
            return 0

        return (

            self.total_processing_time

            /

            self.frames_processed

        )
    
    # --------------------------------------------------------

    def empty(self) -> Dict:
        """
        Returns an empty/default movement analysis.

        Used when there are no active tracks so that the
        pipeline can continue without running analyze().
        """

        return {
            "tracked_people": 0,
            "moving_people": 0,
            "stationary_people": 0,
            "crowd_direction": (0, 0),
            "fastest_track": None,
            "flow_level": "Still",
            "max_speed": 0.0,
            "average_movement": 0.0
        }

    # --------------------------------------------------------

    def clear(self):
        """
        Clears stored movement history.
        """

        self.track_history.clear()

        self.total_distance.clear()

        self.current_speed.clear()

        self.direction.clear()

        self.stationary_frames.clear()

        self.moving_frames.clear()

        self.previous_positions.clear()

    # --------------------------------------------------------

    def tracked_count(self) -> int:
        """
        Returns number of tracked people.
        """

        return len(self.previous_positions)
    
    def info(self):

        return {

            "tracked_people":

                len(self.previous_positions),

            "frames_processed":

                self.frames_processed,

            "processing_time_ms":

                round(

                    self.processing_time*1000,

                    2

                ),

            "average_processing_time_ms":

                round(

                    self.average_processing_time*1000,

                    2

                ),

            "fps":

                round(

                    self.fps,

                    2

                )

        }
    
    def direction_name(dx, dy):

        if abs(dx) > abs(dy):

            return "East" if dx > 0 else "West"

        if abs(dy) > abs(dx):

            return "South" if dy > 0 else "North"

        if dx > 0 and dy < 0:
            return "North-East"

        if dx > 0 and dy > 0:
            return "South-East"

        if dx < 0 and dy < 0:
            return "North-West"

        return "South-West"


# ============================================================
# Singleton
# ============================================================

movement_analyzer = MovementAnalyzer()