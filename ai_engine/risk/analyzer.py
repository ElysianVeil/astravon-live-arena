"""
============================================================
Astravon Live Arena
Risk Analyzer

Purpose:
    Combines crowd statistics and environmental
    conditions to generate an overall event risk
    assessment.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import Dict

from crowd.statistics import CrowdStatistics
from heat.heat_index import HeatIndexCalculator

from .scoring import RiskScorer
from .severity import RiskSeverity
from .recommendations import RecommendationEngine


class RiskAnalyzer:
    """
    Main risk analysis engine.

    This class coordinates all risk components and
    produces one complete risk report.
    """

    def __init__(self):

        self.statistics = CrowdStatistics()

        self.heat_index = HeatIndexCalculator()

        self.scorer = RiskScorer()

        self.severity = RiskSeverity()

        self.recommendations = RecommendationEngine()

    # ========================================================
    # Analyze Risk
    # ========================================================

    def analyze(
        self,
        people_count: int,
        venue_capacity: int,
        density: str,
        occupancy: int,
        temperature: float,
        humidity: float
    ) -> Dict:
        """
        Analyze current event conditions.
        """

        # occupancy = self.statistics.calculate_occupancy(
        #     people_count,
        #     venue_capacity
        # )

        heat_index = self.heat_index.calculate(
            temperature,
            humidity
        )

        score = self.scorer.calculate(
            people_count=people_count,
            occupancy=occupancy,
            density=density,
            heat_index=heat_index
        )

        level = self.severity.classify(score)

        actions = self.recommendations.generate(level)

        return {

            "timestamp": datetime.now().isoformat(),

            "people_count": people_count,

            "venue_capacity": venue_capacity,

            "occupancy": occupancy,

            "density": density,

            "temperature": round(temperature, 2),

            "humidity": round(humidity, 2),

            "heat_index": round(heat_index, 2),

            "risk_score": score,

            "risk_level": level,

            "recommendations": actions
        }

    # ========================================================
    # Simple Analysis
    # ========================================================

    def quick_analysis(
        self,
        statistics: Dict
    ) -> Dict:
        """
        Analyze directly from a statistics dictionary.
        """

        return self.analyze(
            people_count=statistics["people_count"],
            venue_capacity=statistics["venue_capacity"],
            density=statistics["density"],
            temperature=statistics["temperature"],
            humidity=statistics["humidity"]
        )