"""
============================================================
Astravon Live Arena
Crowd Statistics

Purpose:
    Aggregates crowd analytics into a single statistics object
    that can be consumed by the backend dashboard, risk engine,
    reporting system, and websocket broadcaster.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Any
from collections import deque
from config import settings
from constants import VERSION, APP_NAME

# from crowd.congestion import CongestionAnalyzer
# from crowd.density import CrowdDensity
# from crowd.movement import MovementAnalyzer
# from crowd.occupancy import OccupancyAnalyzer
# from vision.detector import YOLODetector
# from vision.drawing import Drawing
# from vision.tracker import PersonTracker


class CrowdStatistics:
    """
    Builds complete crowd statistics from the outputs of the
    crowd analysis pipeline.
    """

    def __init__(self):
        self._latest_statistics = {}

        self.history = deque(maxlen=500)

        # self.occupancy_analyzer = OccupancyAnalyzer()

        # self.congestion_analyzer = CongestionAnalyzer()

        # self.density_analyzer = CrowdDensity()

        # self.movement_analyzer = MovementAnalyzer()

        # self.detector = YOLODetector()

        # self.tracker = PersonTracker()

        # self.drawing = Drawing()

        self.statistics_generated = 0

        self.last_timestamp = None

        self.average_people = 0.0

        self.peak_people = 0

    # ========================================================
    # Build Statistics
    # ========================================================
    def build(
        self,
        camera,
        detector,
        tracker,
        movement,
        feature_extractor,
        identity_database,
        matcher,
        crowd_counter,
        density,
        occupancy,
        congestion,
        trends=None,
        risk=None,
        zones=None,
        performance=None,
        weather=None
    ):
        """
        Creates a complete statistics dictionary.
        """

        people = crowd_counter.get(
            "current_count",
            0
        )

        self.peak_people = max(
            self.peak_people,
            people
        )

        statistics = {

            # ======================================================
            # Metadata
            # ======================================================

            "timestamp": datetime.now().isoformat(),

            "statistics_version": "3.0",

            "engine": {

                "name": APP_NAME,

                "version": VERSION,

                "status": "Running",

                "uptime": performance["uptime_seconds"],

                "generated_statistics": self.statistics_generated

            },

            # ======================================================
            # Camera
            # ======================================================

            "camera": camera,

            # ======================================================
            # Detection
            # ======================================================

            "detection": {

                "people_count": crowd_counter["current_count"],

                "detector": detector

            },

            # ======================================================
            # Tracking
            # ======================================================

            # "tracking": tracking,

            # ======================================================
            # Movement
            # ======================================================

            "movement": movement,

            # ======================================================
            # Density
            # ======================================================

            "density": density,

            # ======================================================
            # Occupancy
            # ======================================================

            "occupancy": occupancy,

            # ======================================================
            # Congestion
            # ======================================================

            "congestion": congestion,

            # ======================================================
            # Risk
            # ======================================================

            "risk": risk,

            # ======================================================
            # Weather
            # ======================================================

            "weather": weather,

            # ======================================================
            # Trends
            # ======================================================

            "trends": trends,

            # ======================================================
            # Zones
            # ======================================================

            "zones": zones,

            # ======================================================
            # Performance
            # ======================================================

            "performance": {

                "average_processing_time": performance["average_processing_time"],

                "processing_time": performance["current_processing_time"],

                "average_fps": performance["average_fps"],

                "current_fps": performance["current_fps"],

                "camera": camera,

                "detector": detector,

                "tracker": tracker,

                "movement": movement,

                "feature_extractor": feature_extractor,

                "identity_database": identity_database,

                "matcher": matcher,

                "counter": crowd_counter,

                "density": density,

                "occupancy": occupancy,

                "congestion": congestion

            }

        }

        self._latest_statistics = statistics

        self.history.append(statistics)

        self.statistics_generated += 1

        self.last_timestamp = statistics["timestamp"]

        return statistics

    # ========================================================
    # Latest Statistics
    # ========================================================

    def latest(self) -> Dict[str, Any]:
        """
        Returns the latest generated statistics.
        """

        return self._latest_statistics
    
    def average_people_count(self):

        if not self.history:
            return 0

        return round(

            sum(

                item["detection"]["people_count"]

                for item in self.history

            )

            /

            len(self.history),

            2

        )
    
    def info(self):

        return {

            "records":

                len(self.history),

            "generated":

                self.statistics_generated,

            "peak_people":

                self.peak_people,

            "average_people":

                self.average_people_count(),

            "last_timestamp":

                self.last_timestamp

        }

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Clears cached statistics.
        """

        self._latest_statistics = {}

        self.history.clear()

        self.statistics_generated = 0

        self.last_timestamp = None

        self.average_people = 0

        self.peak_people = 0

    # ========================================================
    # Summary
    # ========================================================

    def summary(self) -> Dict[str, Any]:
        """
        Returns a simplified statistics summary.
        """

        if not self._latest_statistics:
            return {}

        return {

            "timestamp":

                self.last_timestamp,

            "people":

                self._latest_statistics.get(

                    "detection",

                    {}

                ),

            "weather":
                self._latest_statistics.get(
                    "weather",

                    {}
                ),

            "risk":
                self._latest_statistics.get(
                    "risk",

                    {}
                ),

            "occupancy":

                self._latest_statistics.get(

                    "occupancy",

                    {}

                ),

            "density":

                self._latest_statistics.get(

                    "density",

                    {}

                ),

            "movement":

                self._latest_statistics.get(

                    "movement",

                    {}

                ),

            "congestion":

                self._latest_statistics.get(

                    "congestion",

                    {}

                )

        }


    def as_json(self):

      return self._latest_statistics
    
    def history_list(self):

        return list(self.history)

# ============================================================
# Singleton Instance
# ============================================================

crowd_statistics = CrowdStatistics()