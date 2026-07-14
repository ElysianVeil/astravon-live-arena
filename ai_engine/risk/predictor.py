"""
============================================================
Astravon Live Arena
Risk Predictor

Purpose:
    Predicts future crowd conditions using recent
    crowd statistics and environmental data.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from statistics import mean
from typing import Dict, List


class RiskPredictor:
    """
    Predicts future crowd conditions.

    This predictor uses recent historical values
    rather than machine learning.
    """

    def __init__(self):

        self.history: List[Dict] = []

        self.max_history = 30

    # ========================================================
    # Add Snapshot
    # ========================================================

    def update(
        self,
        snapshot: Dict
    ) -> None:
        """
        Store the latest crowd statistics.
        """

        self.history.append(snapshot)

        if len(self.history) > self.max_history:
            self.history.pop(0)

    # ========================================================
    # Prediction
    # ========================================================

    def predict(self) -> Dict:
        """
        Predict future event conditions.
        """

        if not self.history:

            return {
                "prediction": "Unknown",
                "confidence": 0,
                "expected_people": 0,
                "expected_risk_score": 0,
                "trend": "Unknown",
                "timestamp": datetime.now().isoformat()
            }

        latest = self.history[-1]

        people = [x["people_count"] for x in self.history]
        scores = [x["risk_score"] for x in self.history]

        average_people = round(mean(people))
        average_score = round(mean(scores))

        trend = self._trend(people)

        predicted_people = latest["people_count"]

        if trend == "Increasing":
            predicted_people += 20

        elif trend == "Decreasing":
            predicted_people = max(
                0,
                predicted_people - 20
            )

        prediction = self._prediction_level(
            average_score
        )

        return {

            "prediction": prediction,

            "trend": trend,

            "confidence": self._confidence(),

            "expected_people": predicted_people,

            "expected_risk_score": average_score,

            "timestamp": datetime.now().isoformat()
        }

    # ========================================================
    # Trend Detection
    # ========================================================

    def _trend(
        self,
        values: List[int]
    ) -> str:
        """
        Detect whether values are increasing,
        decreasing or stable.
        """

        if len(values) < 2:
            return "Stable"

        if values[-1] > values[0]:
            return "Increasing"

        if values[-1] < values[0]:
            return "Decreasing"

        return "Stable"

    # ========================================================
    # Risk Prediction
    # ========================================================

    def _prediction_level(
        self,
        score: float
    ) -> str:
        """
        Predict overall risk level.
        """

        if score >= 90:
            return "Critical"

        if score >= 70:
            return "High"

        if score >= 40:
            return "Medium"

        return "Low"

    # ========================================================
    # Confidence
    # ========================================================

    def _confidence(self) -> int:
        """
        Confidence improves as more data
        becomes available.
        """

        confidence = len(self.history) * 4

        return min(confidence, 100)

    # ========================================================
    # Utilities
    # ========================================================

    def clear(self):
        """
        Clears prediction history.
        """

        self.history.clear()

    def history_size(self) -> int:
        """
        Returns number of stored snapshots.
        """

        return len(self.history)