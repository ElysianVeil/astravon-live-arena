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


class CrowdStatistics:
    """
    Builds complete crowd statistics from the outputs of the
    crowd analysis pipeline.
    """

    def __init__(self):
        self._latest_statistics: Dict[str, Any] = {}

    # ========================================================
    # Build Statistics
    # ========================================================

    def build(
        self,
        people_count: int,
        density: str,
        occupancy: float,
        average_speed: float,
        congestion_level: str,
        entering: int,
        leaving: int,
    ) -> Dict[str, Any]:
        """
        Creates a complete statistics dictionary.
        """

        statistics = {
            "timestamp": datetime.now().isoformat(),

            "people_count": people_count,

            "density": density,

            "occupancy": round(occupancy, 2),

            "movement": {
                "average_speed": round(average_speed, 2),
                "entering": entering,
                "leaving": leaving
            },

            "congestion": congestion_level
        }

        self._latest_statistics = statistics

        return statistics

    # ========================================================
    # Latest Statistics
    # ========================================================

    def latest(self) -> Dict[str, Any]:
        """
        Returns the latest generated statistics.
        """

        return self._latest_statistics

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Clears cached statistics.
        """

        self._latest_statistics = {}

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
            "people_count": self._latest_statistics["people_count"],
            "density": self._latest_statistics["density"],
            "occupancy": self._latest_statistics["occupancy"],
            "congestion": self._latest_statistics["congestion"]
        }


# ============================================================
# Singleton Instance
# ============================================================

crowd_statistics = CrowdStatistics()