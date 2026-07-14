"""
============================================================
Astravon Live Arena
Crowd Congestion Analyzer

Purpose:
    Analyzes crowd congestion using crowd count,
    occupancy, density and movement statistics.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import Dict


# ============================================================
# Congestion Analyzer
# ============================================================

class CongestionAnalyzer:
    """
    Determines congestion severity.
    """

    def __init__(self):

        self.history = []

    # --------------------------------------------------------

    def calculate_score(
        self,
        occupancy_percentage: float,
        people_per_square_meter: float,
        average_movement: float
    ) -> float:
        """
        Calculates congestion score (0-100).
        """

        score = 0.0

        # --------------------------------------------
        # Occupancy Contribution (40)
        # --------------------------------------------

        score += min(
            occupancy_percentage,
            100
        ) * 0.40

        # --------------------------------------------
        # Density Contribution (40)
        # --------------------------------------------

        density_score = min(
            people_per_square_meter * 20,
            40
        )

        score += density_score

        # --------------------------------------------
        # Movement Contribution (20)
        #
        # Lower movement generally means
        # greater congestion.
        # --------------------------------------------

        if average_movement < 5:
            score += 20

        elif average_movement < 10:
            score += 15

        elif average_movement < 20:
            score += 8

        return round(score, 2)

    # --------------------------------------------------------

    def congestion_level(
        self,
        score: float
    ) -> str:
        """
        Converts score into a congestion level.
        """

        if score < 25:
            return "Free Flow"

        if score < 50:
            return "Moderate"

        if score < 70:
            return "Busy"

        if score < 90:
            return "Congested"

        return "Critical"

    # --------------------------------------------------------

    def recommendation(
        self,
        level: str
    ) -> str:
        """
        Returns an action recommendation.
        """

        recommendations = {

            "Free Flow":
                "No action required.",

            "Moderate":
                "Continue monitoring.",

            "Busy":
                "Increase surveillance.",

            "Congested":
                "Prepare crowd management personnel.",

            "Critical":
                "Immediate intervention recommended."
        }

        return recommendations.get(
            level,
            "Continue monitoring."
        )

    # --------------------------------------------------------

    def analyze(
        self,
        people_count: int,
        occupancy_percentage: float,
        people_per_square_meter: float,
        average_movement: float
    ) -> Dict:
        """
        Performs complete congestion analysis.
        """

        score = self.calculate_score(
            occupancy_percentage,
            people_per_square_meter,
            average_movement
        )

        level = self.congestion_level(
            score
        )

        result = {

            "people_count": people_count,

            "occupancy_percentage":
                occupancy_percentage,

            "people_per_square_meter":
                people_per_square_meter,

            "average_movement":
                average_movement,

            "congestion_score":
                score,

            "congestion_level":
                level,

            "recommendation":
                self.recommendation(level)
        }

        self.history.append(result)

        return result

    # --------------------------------------------------------

    def latest(self) -> Dict:
        """
        Returns latest congestion analysis.
        """

        if not self.history:
            return {}

        return self.history[-1]

    # --------------------------------------------------------

    def clear(self):
        """
        Clears history.
        """

        self.history.clear()

    # --------------------------------------------------------

    def total_records(self) -> int:
        """
        Returns number of analyses.
        """

        return len(self.history)


# ============================================================
# Singleton
# ============================================================

congestion_analyzer = CongestionAnalyzer()