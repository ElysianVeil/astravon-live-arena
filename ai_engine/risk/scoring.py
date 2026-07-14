"""
============================================================
Astravon Live Arena
Risk Scoring Engine

Purpose:
    Calculates an overall event risk score based on
    crowd statistics and environmental conditions.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import Union


class RiskScorer:
    """
    Calculates a numerical risk score.

    The final score ranges from 0 to 100 and is
    calculated using crowd occupancy, density,
    and heat index.
    """

    def __init__(self):

        self.max_score = 100

    # ========================================================
    # Public API
    # ========================================================

    def calculate(
        self,
        people_count: int,
        occupancy: float,
        density: str,
        heat_index: float
    ) -> int:
        """
        Calculates the overall risk score.

        Returns:
            Integer between 0 and 100.
        """

        score = 0.0

        score += self._occupancy_score(occupancy)

        score += self._density_score(density)

        score += self._heat_score(heat_index)

        score += self._crowd_size_score(people_count)

        score = min(score, self.max_score)

        return round(score)

    # ========================================================
    # Occupancy
    # ========================================================

    def _occupancy_score(
        self,
        occupancy: float
    ) -> float:
        """
        Scores venue occupancy.

        Maximum contribution: 35
        """

        if occupancy >= 100:
            return 35

        return (occupancy / 100) * 35

    # ========================================================
    # Crowd Density
    # ========================================================

    def _density_score(
        self,
        density: str
    ) -> float:
        """
        Scores crowd density.

        Maximum contribution: 25
        """

        density = density.lower()

        scores = {
            "low": 5,
            "medium": 15,
            "high": 25
        }

        return scores.get(density, 0)

    # ========================================================
    # Heat
    # ========================================================

    def _heat_score(
        self,
        heat_index: float
    ) -> float:
        """
        Scores environmental heat.

        Maximum contribution: 25
        """

        if heat_index >= 54:
            return 25

        if heat_index >= 41:
            return 20

        if heat_index >= 32:
            return 15

        if heat_index >= 27:
            return 10

        return 5

    # ========================================================
    # Crowd Size
    # ========================================================

    def _crowd_size_score(
        self,
        people_count: int
    ) -> float:
        """
        Larger crowds generally increase risk.

        Maximum contribution: 15
        """

        if people_count >= 1000:
            return 15

        if people_count >= 500:
            return 12

        if people_count >= 250:
            return 9

        if people_count >= 100:
            return 6

        if people_count >= 50:
            return 3

        return 1

    # ========================================================
    # Utility
    # ========================================================

    def normalize(
        self,
        value: Union[int, float]
    ) -> int:
        """
        Clamp a value to the valid score range.
        """

        value = max(0, value)
        value = min(value, self.max_score)

        return round(value)