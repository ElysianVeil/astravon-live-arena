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
from utils.logger import get_logger
from collections import deque
from config import settings

logger = get_logger("Congestion Analyzer")


# ============================================================
# Congestion Analyzer
# ============================================================

class CongestionAnalyzer:
    """
    Determines congestion severity.
    """

    def __init__(self):



        self.history = deque(maxlen=300)

        self.current_score = 0.0

        self.peak_score = 0.0

        self.average_score = 0.0

        self.current_level = settings.OCCUPANCY_EMPTY

        self.last_people_count = 0

        self.last_density = 0.0

        self.last_movement = 0.0

        self.last_recommendation = ""

        self.frames_processed = 0

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
        ) * settings.CONGESTION_OCCUPANCY_WEIGHT

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
    
    def risk_level(
        self,
        score
    ):

        if score < 40:
            return "LOW"

        elif score < 60:
            return "MEDIUM"

        elif score < 80:
            return "HIGH"

        return "CRITICAL"
    
    def crowd_stability(
        self,
        average_speed
    ):

        if average_speed < 2:
            return "Stationary"

        elif average_speed < 8:
            return "Slow"

        elif average_speed < 15:
            return "Normal"

        return "Fast"
    
    def congestion_trend(self):

        if len(self.history) < 2:
            return "Stable"

        previous = self.history[-2]["congestion_score"]

        current = self.history[-1]["congestion_score"]

        if current > previous:
            return "Increasing"

        elif current < previous:
            return "Decreasing"

        return "Stable"
    
    def average_congestion(self):

        if not self.history:
            return 0

        return round(

            sum(

                item["congestion_score"]

                for item in self.history

            )

            /

            len(self.history),

            2

        )
    
    def peak_congestion(self):

        if not self.history:
            return 0

        return max(

            item["congestion_score"]

            for item in self.history

        )
    
    def incident_probability(
        self,
        score
    ):

        if score < 40:
            return 0.05

        elif score < 60:
            return 0.20

        elif score < 80:
            return 0.55

        return 0.90

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

        recommendation = self.recommendation(level)

        change = (

            score -

            self.current_score

        )

        result = {

            "people_count": people_count,

            "occupancy_percentage": occupancy_percentage,

            "people_per_square_meter": people_per_square_meter,

            "average_speed": average_movement,

            "congestion_score": score,

            "congestion_level": level,

            "risk_level": self.risk_level(score),

            "stability": self.crowd_stability(
                average_movement
            ),

            "trend": self.congestion_trend(),

            "score_change": change,

            "incident_probability":
                self.incident_probability(score),

            "recommendation":
                recommendation

        }
        logger.info(

            f"Congestion "

            f"{score:.1f}/100 "

            f"({level})"

        )
        self.history.append(result)
        self.current_score = score

        self.current_level = level

        self.last_people_count = people_count

        self.last_density = people_per_square_meter

        self.last_speed = average_movement

        self.last_recommendation = recommendation

        self.frames_processed += 1

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

        self.current_score = 0

        self.current_level = settings.OCCUPANCY_EMPTY

        self.peak_score = 0

        self.average_score = 0

        self.frames_processed = 0

        self.last_people_count = 0

        self.last_density = 0

        self.last_speed = 0

        self.last_recommendation = ""

    # --------------------------------------------------------

    def total_records(self) -> int:
        """
        Returns number of analyses.
        """

        return len(self.history)
    
    def summary(self):

        return {

            "frames_processed":

                self.frames_processed,

            "current_score":

                self.current_score,

            "current_level":

                self.current_level,

            "peak_score":

                self.peak_congestion(),

            "average_score":

                self.average_congestion(),

            "trend":

                self.congestion_trend()

        }


# ============================================================
# Singleton
# ============================================================

congestion_analyzer = CongestionAnalyzer()