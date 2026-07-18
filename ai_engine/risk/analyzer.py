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
from collections import deque

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

        self.history = deque(maxlen=1000)

        self.last_analysis = None

        self.total_analyses = 0

        self.high_risk_events = 0

        self.critical_events = 0

        self.maximum_risk_score = 0

        self.minimum_risk_score = 100

        self.total_risk_score = 0

        self.average_risk_score = 0

        self.last_prediction = None

        self.engine_status = "Running"

    # ========================================================
    # Analyze Risk
    # ========================================================

    def analyze(
        self,
        people_count: int,
        venue_capacity: int,
        density: str,
        occupancy: int,
        movement: Dict,
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

        average_speed = movement["average_movement"]

        flow_level = movement["flow_level"]

        moving_people = movement["moving_people"]

        stationary_people = movement["stationary_people"]

        heat = self.heat_index.reading(
            temperature,
            humidity
        )

        heat_index = heat["heat_index"]

        score = self.scorer.calculate(
            people_count=people_count,
            occupancy=occupancy,
            density=density,
            heat_index=heat_index
        )

        level = self.severity.classify(score)

        actions = self.recommendations.generate(
            level=level,
            people_count=people_count,
            occupancy=occupancy,
            density=density,
            heat_index=heat_index,
            movement=flow_level

        )

        report = {

            "timestamp": datetime.now().isoformat(),

            "people_count": people_count,

            "venue_capacity": venue_capacity,

            "occupancy": occupancy,

            "density": density,

            "movement": {

                "average_speed": average_speed,

                "flow_level": flow_level,

                "moving_people": moving_people,

                "stationary_people": stationary_people

            },

            "temperature": round(temperature, 2),

            "humidity": round(humidity, 2),

            "heat": heat,

            "risk_score": score,

            "risk_level": level,

            "recommendations": actions
        }

        self.total_analyses += 1

        self.last_analysis = report

        self.history.append(report)

        self.maximum_risk_score = max(
            self.maximum_risk_score,
            score
        )

        self.minimum_risk_score = min(
            self.minimum_risk_score,
            score
        )

        self.total_risk_score += score

        self.average_risk_score = round(
            self.total_risk_score /
            self.total_analyses,
            2
        )

        if level == "High":
            self.high_risk_events += 1

        if level == "Critical":
            self.critical_events += 1

        return report

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

            occupancy=statistics["occupancy"],

            movement=statistics["movement"],

            temperature=statistics["temperature"],

            humidity=statistics["humidity"]

        )
    
    # ========================================================
    # Predict Risk
    # ========================================================

    def predict(self):

        if len(self.history) < 5:
            return None

        scores = [
            r["risk_score"]
            for r in list(self.history)[-5:]
        ]

        prediction = round(sum(scores) / len(scores), 2)

        self.last_prediction = prediction

        return {

            "predicted_risk": prediction,

            "predicted_level":
                self.severity.classify(prediction)

        }
    
    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):

        return {

            "total_analyses":
                self.total_analyses,

            "maximum_risk_score":
                self.maximum_risk_score,

            "minimum_risk_score":
                self.minimum_risk_score,

            "average_risk_score":
                self.average_risk_score,

            "high_risk_events":
                self.high_risk_events,

            "critical_events":
                self.critical_events,

            "latest":
                self.last_analysis

        }
    
    # ========================================================
    # Summary
    # ========================================================

    def summary(self):

        if self.last_analysis is None:

            return {}

        return {

            "risk_score":
                self.last_analysis["risk_score"],

            "risk_level":
                self.last_analysis["risk_level"],

            "recommendations":
                self.last_analysis["recommendations"],

            "heat":
                self.last_analysis["heat"],

            "movement":
                self.last_analysis["movement"]

        }
    
    # ========================================================
    # Search
    # ========================================================

    def search(
        self,
        minimum_score=None,
        level=None
    ):

        results = []

        for report in self.history:

            if minimum_score is not None:

                if report["risk_score"] < minimum_score:
                    continue

            if level is not None:

                if report["risk_level"] != level:
                    continue

            results.append(report)

        return results
    
    # ========================================================
    # History
    # ========================================================

    def get_history(self):

        return list(self.history)
    
    # ========================================================
    # Information
    # ========================================================

    def info(self):

        return {

            "module":
                "Risk Analyzer",

            "status":
                self.engine_status,

            "history":
                len(self.history),

            "total_analyses":
                self.total_analyses,

            "high_risk_events":
                self.high_risk_events,

            "critical_events":
                self.critical_events,

            "latest":
                (
                    self.last_analysis["timestamp"]
                    if self.last_analysis
                    else None
                )

        }
    
    # ========================================================
    # Reset
    # ========================================================

    def reset(self):

        self.history.clear()

        self.last_analysis = None

        self.total_analyses = 0

        self.high_risk_events = 0

        self.critical_events = 0

        self.maximum_risk_score = 0

        self.minimum_risk_score = 100

        self.total_risk_score = 0

        self.average_risk_score = 0

        self.last_prediction = None

        self.engine_status = "Running"

    # ========================================================
    # Alert Required
    # ========================================================

    def requires_alert(
        self,
        score: float
    ):

        return score >= 70
    
    # ========================================================
    # Risk Trend
    # ========================================================

    def trend(self):

        if len(self.history) < 3:
            return "Stable"

        recent = list(self.history)[-3:]

        scores = [
            r["risk_score"]
            for r in recent
        ]

        if scores[-1] > scores[0]:
            return "Increasing"

        if scores[-1] < scores[0]:
            return "Decreasing"

        return "Stable"