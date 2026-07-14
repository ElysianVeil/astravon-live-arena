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

        self.history: Deque[Dict] = deque(
            maxlen=max_history
        )

    # ========================================================
    # Add Record
    # ========================================================

    def add(
        self,
        people_count: int,
        density: str,
        occupancy: float,
        risk_score: int
    ) -> None:
        """
        Adds a new crowd record.
        """

        self.history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "people_count": people_count,
                "density": density,
                "occupancy": occupancy,
                "risk_score": risk_score
            }
        )

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
            "direction": self.direction(),
            "growth_rate": self.growth_rate()
        }

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Clears all stored history.
        """

        self.history.clear()


# ============================================================
# Singleton
# ============================================================

crowd_trends = CrowdTrends()