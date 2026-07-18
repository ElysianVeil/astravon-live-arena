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

        # Weight configuration
        self.weights = {

            "occupancy": 0.20,
            "density": 0.15,
            "heat": 0.15,
            "crowd_size": 0.10,
            "movement": 0.10,
            "congestion": 0.10,
            "weather": 0.05,
            "history": 0.05,
            "trend": 0.05,
            "prediction": 0.05
        }

    # ========================================================
    # Public API
    # ========================================================

    def calculate(

        self,

        people_count: int,

        occupancy: float,

        density: str,

        heat_index: float,

        movement: dict | None = None,

        congestion: dict | None = None,

        weather: dict | None = None,

        trend: dict | None = None,

        prediction: dict | None = None

    ) -> int:
        """
        Calculates the overall risk score.

        Returns:
            Integer between 0 and 100.
        """

        score = 0.0

        score += (
            self._occupancy_score(occupancy)
            * self.weights["occupancy"]
        )

        score += (
            self._density_score(density)
            * self.weights["density"]
        )

        score += (
            self._heat_score(heat_index)
            * self.weights["heat"]
        )

        score += (
            self._crowd_size_score(people_count)
            * self.weights["crowd_size"]
        )

        if movement:

            score += (

                self._movement_score(movement)

                *

                self.weights["movement"]

            )

        score = min(score, self.max_score)

        return round(score)
    
    # ========================================================
    # Breakdown
    # ========================================================

    def breakdown(

        self,

        people_count,

        occupancy,

        density,

        heat_index

    ):

        return {

            "occupancy":
                self._occupancy_score(
                    occupancy
                ),

            "density":
                self._density_score(
                    density
                ),

            "heat":
                self._heat_score(
                    heat_index
                ),

            "crowd":
                self._crowd_size_score(
                    people_count
                )

        }
    
    def percentage(
        self,
        score
    ):

        return round(

            score

            /

            self.max_score

            *

            100,

            2

        )
    
    def color(
        self,
        score
    ):

        if score < 20:
            return "#2ECC71"

        if score < 40:
            return "#F1C40F"

        if score < 60:
            return "#F39C12"

        if score < 80:
            return "#E67E22"

        return "#E74C3C"
    
    def gauge_zone(
        self,
        score
    ):

        if score < 20:
            return "Safe"

        elif score < 40:
            return "Monitor"

        elif score < 60:
            return "Warning"

        elif score < 80:
            return "Danger"

        return "Critical"
    
    def label(
        self,
        score
    ):

        return f"{score}/100"
    
    def explain(

        self,

        people_count,

        occupancy,

        density,

        heat_index

    ):

        breakdown = self.breakdown(

            people_count,

            occupancy,

            density,

            heat_index

        )

        return {

            "breakdown": breakdown,

            "highest_factor": max(

                breakdown,

                key=breakdown.get

            )

        }
    
    # ========================================================
    # Module Information
    # ========================================================

    def info(self):

        return {

            "module":"Risk Scorer",

            "version":"2.0.0",

            "maximum_score":self.max_score,

            "weights":self.weights

        }

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

            "free flow":5,

            "low":10,

            "medium":20,

            "busy":30,

            "high":40,

            "critical":50

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

        if heat_index < 27:
            return 5

        elif heat_index < 32:
            return 20

        elif heat_index < 41:
            return 40

        elif heat_index < 54:
            return 70

        return 100

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

        if people_count >= 5000:
            return 100

        elif people_count >= 2500:
            return 80

        elif people_count >= 1000:
            return 60

        elif people_count >= 500:
            return 40

        elif people_count >= 100:
            return 20

        return 5

    # ========================================================
    # Movement
    # ========================================================

    def _movement_score(
        self,
        movement: dict
    ) -> float:

        flow = movement.get(
            "flow_level",
            "Low"
        ).lower()

        scores = {

            "low":20,

            "medium":40,

            "high":70,

            "panic":100

        }

        return scores.get(flow,20)
    
    # ========================================================
    # Congestion
    # ========================================================

    def _congestion_score(
        self,
        congestion: dict
    ) -> float:

        return min(

            100,

            congestion.get(
                "score",
                0
            )

        )
    
    # ========================================================
    # Weather
    # ========================================================

    def _weather_score(
        self,
        weather: dict
    ):

        score = 0

        if weather["wind_speed"] > 25:
            score += 25

        if weather["rain_probability"] > 60:
            score += 25

        if weather["uv_index"] > 8:
            score += 25

        if weather["weather_code"] in [95]:
            score += 25

        return score
    
    def _trend_score(
        self,
        trend: dict
    ):

        if trend["risk"] == "Increasing":

            return 100

        if trend["risk"] == "Stable":

            return 50

        return 10
    
    def _prediction_score(
        self,
        prediction: dict
    ):

        return prediction.get(
            "predicted_risk_score",
            0
        )

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