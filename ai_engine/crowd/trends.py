"""
============================================================
Astravon Live Arena
Crowd Trends

Purpose:
    Tracks crowd trends over time and provides simple
    analytics such as increasing, decreasing, or stable
    crowd movement.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from collections import deque
from datetime import datetime
from statistics import mean
import time
from typing import Deque, Dict, List


class CrowdTrends:
    """
    Stores crowd history and performs trend analysis.
    """

    def __init__(
        self,
        max_history: int = 300
    ):
        """
        Args:
            max_history:
                Maximum number of records kept.
        """

        self.max_history = max_history
        # Performance metrics
        self.records_added = 0
        self.processing_time = 0.0
        self.total_processing_time = 0.0

        self.history: Deque[Dict] = deque(
            maxlen=max_history
        )

    # ========================================================
    # Add Record
    # ========================================================

    def add(
        self,
        people_count,
        density,
        occupancy,
        risk_score,
        average_speed=0,
        moving_people=0,
        stationary_people=0,
        flow_level="Still"
    ):
        """
        Adds a new crowd record.
        """
        start = time.perf_counter()

        self.history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "people_count": people_count,
                "density": density,
                "occupancy": occupancy,
                "risk_score": risk_score,
                "average_speed": average_speed,
                "moving_people": moving_people,
                "stationary_people": stationary_people,
                "flow_level": flow_level
            }
        )

        elapsed = time.perf_counter() - start

        self.processing_time = elapsed
        self.total_processing_time += elapsed
        self.records_added += 1

    # ========================================================
    # History
    # ========================================================

    def get_history(self) -> List[Dict]:
        """
        Returns all stored history.
        """

        return list(self.history)

    # ========================================================
    # Latest
    # ========================================================

    def latest(self) -> Dict:
        """
        Returns the newest record.
        """

        if not self.history:
            return {}

        return self.history[-1]

    # ========================================================
    # Average Crowd
    # ========================================================

    def average_people(self) -> float:
        """
        Average crowd size.
        """

        if not self.history:
            return 0.0

        return round(
            mean(
                item["people_count"]
                for item in self.history
            ),
            2
        )
    
    def average_speed(self):

        if not self.history:
            return 0

        return round(

            mean(
                item["average_speed"]
                for item in self.history
            ),

            2

        )
    
    def average_risk(self):

        if not self.history:
            return 0

        return round(

            mean(
                item["risk_score"]
                for item in self.history
            ),

            2

        )

    def peak_risk(self):

        if not self.history:
            return 0

        return max(

            item["risk_score"]

            for item in self.history

        )
    
    def average_occupancy(self):

        if not self.history:
            return 0

        return round(

            mean(
                item["occupancy"]

                for item in self.history
            ),

            2

        )
    
    def peak_occupancy(self):

        if not self.history:
            return 0

        return max(

            item["occupancy"]

            for item in self.history

        )
    
    def pressure(self):

        latest = self.latest()

        if not latest:
            return "Unknown"

        occupancy = latest["occupancy"]

        if occupancy < 25:
            return "Low"

        elif occupancy < 50:
            return "Moderate"

        elif occupancy < 75:
            return "High"

        return "Critical"
    
    def stability(self):

        if len(self.history) < 10:
            return "Unknown"

        values = [

            item["people_count"]

            for item in self.history

        ]

        variation = max(values) - min(values)

        if variation < 5:
            return "Stable"

        elif variation < 20:
            return "Moderately Stable"

        return "Unstable"
    
    def momentum(self):

        if len(self.history) < 5:
            return 0

        recent = [

            item["people_count"]

            for item in list(self.history)[-5:]

        ]

        return round(

            recent[-1] - recent[0],

            2

        )
    
    def export(self):

        return {

            "history":

                self.get_history(),

            "summary":

                self.summary()

        }
    

    # ========================================================
    # Peak Crowd
    # ========================================================

    def peak_people(self) -> int:
        """
        Highest recorded crowd.
        """

        if not self.history:
            return 0

        return max(
            item["people_count"]
            for item in self.history
        )

    # ========================================================
    # Lowest Crowd
    # ========================================================

    def minimum_people(self) -> int:
        """
        Lowest recorded crowd.
        """

        if not self.history:
            return 0

        return min(
            item["people_count"]
            for item in self.history
        )

    # ========================================================
    # Trend Direction
    # ========================================================

    def direction(self) -> str:
        """
        Determines whether the crowd is increasing,
        decreasing or stable.
        """

        if len(self.history) < 2:
            return "Stable"

        previous = self.history[-2]["people_count"]
        current = self.history[-1]["people_count"]

        if current > previous:
            return "Increasing"

        if current < previous:
            return "Decreasing"

        return "Stable"

    # ========================================================
    # Growth Rate
    # ========================================================

    def growth_rate(self) -> float:
        """
        Percentage change from previous sample.
        """

        if len(self.history) < 2:
            return 0.0

        previous = self.history[-2]["people_count"]
        current = self.history[-1]["people_count"]

        if previous == 0:
            return 0.0

        return round(
            ((current - previous) / previous) * 100,
            2
        )

    # ========================================================
    # Summary
    # ========================================================

    def summary(self) -> Dict:
        """
        Returns a trend summary.
        """

        return {
            "records": len(self.history),
            "latest_people_count": (
                self.latest().get("people_count", 0)
            ),
            "average_people": self.average_people(),
            "peak_people": self.peak_people(),
            "minimum_people": self.minimum_people(),
            "average_speed":

                self.average_speed(),

            "average_risk":

                self.average_risk(),

            "peak_risk":

                self.peak_risk(),

            "average_occupancy":

                self.average_occupancy(),

            "peak_occupancy":

                self.peak_occupancy(),

            "pressure":

                self.pressure(),

            "direction":

                self.direction(),

            "growth_rate":

                self.growth_rate(),

            "momentum":

                self.momentum(),

            "stability":

                self.stability()

        }
    
    @property
    def fps(self):

        if self.processing_time == 0:
            return 0

        return 1 / self.processing_time


    @property
    def average_processing_time(self):

        if self.records_added == 0:
            return 0

        return (
            self.total_processing_time
            /
            self.records_added
        )
    
    def info(self):

        return {

            "records":

                len(self.history),

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

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Clears all stored history.
        """

        self.history.clear()

        self.records_added = 0

        self.processing_time = 0

        self.total_processing_time = 0


# ============================================================
# Singleton
# ============================================================

crowd_trends = CrowdTrends()