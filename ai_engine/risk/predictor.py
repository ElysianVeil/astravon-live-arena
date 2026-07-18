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
from collections import deque


class RiskPredictor:
    """
    Predicts future crowd conditions.

    This predictor uses recent historical values
    rather than machine learning.
    """

    def __init__(self):

        self.history = deque(maxlen=300)

        self.last_prediction = None

        self.total_predictions = 0

        self.maximum_predicted_people = 0

        self.maximum_predicted_risk = 0

        self.prediction_accuracy = []

        self.forecast_minutes = 5

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

        required = {

            "people_count",

            "risk_score",

            "occupancy",

            "density",

            "temperature",

            "heat_index"

        }

        if not required.issubset(snapshot):

            raise ValueError(

                "Invalid prediction snapshot."

            )

        self.history.append(snapshot)

        # if len(self.history) > self.max_history:
        #     self.history.pop(0)

    # ========================================================
    # Average Trend
    # ========================================================

    def average_people(self):

        if not self.history:
            return 0

        return round(

            mean(

                x["people_count"]

                for x in self.history

            )

        )
    
    # ========================================================
    # Average Risk
    # ========================================================

    def average_risk(self):

        if not self.history:
            return 0

        return round(

            mean(

                x["risk_score"]

                for x in self.history

            ),

            2

        )
    
    # ========================================================
    # Average Risk
    # ========================================================

    def average_risk(self):

        if not self.history:
            return 0

        return round(

            mean(

                x["risk_score"]

                for x in self.history

            ),

            2

        )
    

    def risk_velocity(self):

        if len(self.history) < 2:

            return 0

        return (

            self.history[-1]["risk_score"]

            -

            self.history[-2]["risk_score"]

        )

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
                "trend": "Unknown",
                "risk_trend": "Unknown",
                "occupancy_trend": "Unknown",
                "heat_trend": "Unknown",
                "crowd_velocity": 0,
                "risk_velocity": 0,
                "expected_people": 0,
                "expected_occupancy": 0,
                "expected_density": "Unknown",
                "expected_risk_score": 0,
                "recommendation": "Insufficient data",
                "alert_required": False,
                "forecast_minutes": self.forecast_minutes,
                "timestamp": datetime.now().isoformat()
            }

        latest = self.history[-1]

        # --------------------------------------------------
        # Historical Values
        # --------------------------------------------------

        people = [
            item["people_count"]
            for item in self.history
        ]

        # --------------------------------------------------
        # Trends
        # --------------------------------------------------

        crowd_trend = self._trend(people)

        risk_trend = self.risk_trend()

        occupancy_trend = self.occupancy_trend()

        heat_trend = self.heat_trend()

        # --------------------------------------------------
        # Velocities
        # --------------------------------------------------

        crowd_velocity = self.crowd_velocity()

        risk_velocity = self.risk_velocity()

        # --------------------------------------------------
        # Predict People
        # --------------------------------------------------

        predicted_people = max(
            0,
            latest["people_count"] + crowd_velocity
        )

        # --------------------------------------------------
        # Predict Occupancy
        # --------------------------------------------------

        predicted_occupancy = min(
            100,
            max(
                0,
                latest["occupancy"] + (crowd_velocity * 0.1)
            )
        )

        # --------------------------------------------------
        # Predict Density
        # --------------------------------------------------

        if predicted_occupancy >= 90:

            predicted_density = "High"

        elif predicted_occupancy >= 60:

            predicted_density = "Medium"

        else:

            predicted_density = "Low"

        # --------------------------------------------------
        # Predict Risk Score
        # --------------------------------------------------

        predicted_risk = min(
            100,
            max(
                0,
                latest["risk_score"] + risk_velocity
            )
        )

        prediction = self._prediction_level(
            predicted_risk
        )

        # --------------------------------------------------
        # Recommendation
        # --------------------------------------------------

        if predicted_risk >= 90:

            recommendation = "Immediate intervention"

        elif predicted_risk >= 70:

            recommendation = "Deploy additional security and medical staff"

        elif predicted_risk >= 40:

            recommendation = "Increase monitoring"

        else:

            recommendation = "Normal monitoring"

        alert_required = predicted_risk >= 70

        # --------------------------------------------------
        # Build Prediction
        # --------------------------------------------------

        prediction_result = {

            "prediction": prediction,

            "confidence": self._confidence(),

            "trend": crowd_trend,

            "risk_trend": risk_trend,

            "occupancy_trend": occupancy_trend,

            "heat_trend": heat_trend,

            "crowd_velocity": crowd_velocity,

            "risk_velocity": risk_velocity,

            "expected_people": predicted_people,

            "expected_occupancy": round(predicted_occupancy, 2),

            "expected_density": predicted_density,

            "expected_risk_score": round(predicted_risk, 2),

            "recommendation": recommendation,

            "alert_required": alert_required,

            "forecast_minutes": self.forecast_minutes,

            "timestamp": datetime.now().isoformat()
        }

        # --------------------------------------------------
        # Update Statistics
        # --------------------------------------------------

        self.last_prediction = prediction_result

        self.total_predictions += 1

        self.maximum_predicted_people = max(
            self.maximum_predicted_people,
            predicted_people
        )

        self.maximum_predicted_risk = max(
            self.maximum_predicted_risk,
            predicted_risk
        )

        return prediction_result
    
    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):

        return {

            "history_size": len(self.history),

            "total_predictions": self.total_predictions,

            "maximum_predicted_people":

                self.maximum_predicted_people,

            "maximum_predicted_risk":

                self.maximum_predicted_risk,

            "forecast_minutes":

                self.forecast_minutes

        }
    
    def summary(self):

        return (

            self.last_prediction

            if self.last_prediction

            else self.predict()

        )
    
    def info(self):

        return {

            "module":"Risk Predictor",

            "status":"Running",

            "history_size":len(self.history),

            "forecast_minutes":self.forecast_minutes,

            "latest_prediction":(

                self.last_prediction["timestamp"]

                if self.last_prediction

                else None

            )

        }

    def get_history(self):

        return list(self.history)

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

        difference = values[-1] - values[0]

        if abs(difference) < 5:

            return "Stable"

        if difference > 0:

            return "Increasing"

        return "Decreasing"
    
    # ========================================================
    # Crowd Velocity
    # ========================================================

    def crowd_velocity(self) -> int:
        """
        Estimates how quickly the crowd size is changing.

        Returns:
            Positive value  -> Crowd increasing
            Negative value  -> Crowd decreasing
            Zero            -> Stable crowd
        """

        if len(self.history) < 2:
            return 0

        # ---------------------------------------------
        # Use the last five samples if available
        # ---------------------------------------------

        samples = self.history[-5:]

        people = [
            item["people_count"]
            for item in samples
        ]

        # ---------------------------------------------
        # Calculate average frame-to-frame change
        # ---------------------------------------------

        differences = [

            people[i] - people[i - 1]

            for i in range(1, len(people))

        ]

        if not differences:
            return 0

        velocity = sum(differences) / len(differences)

        return round(velocity)
    
    def risk_trend(self):

        scores = [

            x["risk_score"]

            for x in self.history

        ]

        return self._trend(scores)
    
    def occupancy_trend(self):

        occupancy = [

            x["occupancy"]

            for x in self.history

        ]

        return self._trend(occupancy)
    
    def heat_trend(self):

        heat = [

            x["heat_index"]

            for x in self.history

        ]

        return self._trend(heat)

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

        self.history.clear()

        self.last_prediction = None

        self.total_predictions = 0

        self.maximum_predicted_people = 0

        self.maximum_predicted_risk = 0

        self.prediction_accuracy.clear()

    def set_forecast_minutes(

        self,

        minutes:int

    ):

        self.forecast_minutes = max(

            1,

            minutes

        )

    def set_forecast_minutes(

        self,

        minutes:int

    ):

        self.forecast_minutes = max(

            1,

            minutes

        )

    def history_size(self) -> int:
        """
        Returns number of stored snapshots.
        """

        return len(self.history)