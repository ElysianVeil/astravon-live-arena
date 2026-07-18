"""
============================================================
Astravon Live Arena
Heat Index Calculator

Purpose:
    Calculates the apparent temperature (Heat Index)
    using temperature and humidity values.

    Supports crowd safety analysis and risk prediction.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict
from collections import deque
from statistics import mean
import math


class HeatIndexCalculator:
    """
    Calculates heat index values.
    """
    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self):

        self._history = deque(maxlen=500)

        self.maximum_heat_index = 0.0

        self.minimum_heat_index = float("inf")

        self.total_heat_index = 0.0

        self.total_readings = 0

        self.last_reading = None

        self.formula = "NOAA Regression + Simplified"


    # ========================================================
    # Calculate Heat Index
    # ========================================================

    def calculate(
        self,
        temperature: float,
        humidity: float
    ) -> float:
        """
        Calculates the heat index.

        Uses:
         > Simplified approximation
         > NOAA regression
        suitable
        for the MVP.
        """

        humidity = max(0.0, min(100.0, humidity))
        temperature = max(-50.0, min(70.0, temperature))

        # Mild conditions
        if temperature < 27 or humidity < 40:

            hi = temperature + ((humidity / 100.0) * 5)

            return round(hi, 2)

        # NOAA regression
        T = temperature
        RH = humidity

        hi = (
            -8.784695
            + 1.61139411 * T
            + 2.338549 * RH
            - 0.14611605 * T * RH
            - 0.012308094 * (T ** 2)
            - 0.016424828 * (RH ** 2)
            + 0.002211732 * (T ** 2) * RH
            + 0.00072546 * T * (RH ** 2)
            - 0.000003582 * (T ** 2) * (RH ** 2)
        )

        return round(hi, 2)

    # ========================================================
    # Heat Status
    # ========================================================

    def status(
        self,
        heat_index: float
    ) -> str:
        """
        Classifies the heat index.
        """

        if heat_index < 27:
            return "Normal"

        if heat_index < 32:
            return "Caution"

        if heat_index < 41:
            return "Extreme Caution"

        if heat_index < 54:
            return "Danger"

        return "Extreme Danger"
    
    def severity(
        self,
        heat_index: float
    ) -> str:

        if heat_index < 27:
            return "Low"

        if heat_index < 32:
            return "Moderate"

        if heat_index < 41:
            return "High"

        if heat_index < 54:
            return "Critical"

        return "Extreme"
    
    def comfort(
        self,
        heat_index: float
    ) -> str:

        if heat_index < 27:
            return "Comfortable"

        if heat_index < 32:
            return "Warm"

        if heat_index < 41:
            return "Hot"

        if heat_index < 54:
            return "Very Hot"

        return "Dangerous"
    
    def heatstroke_probability(
        self,
        heat_index: float
    ) -> float:

        probability = min(
            100.0,
            max(
                0.0,
                (heat_index - 25) * 3
            )
        )

        return round(probability, 2)

    def recommendation(
        self,
        heat_index: float
    ) -> str:

        if heat_index < 27:
            return "Continue monitoring."

        if heat_index < 32:
            return "Increase hydration."

        if heat_index < 41:
            return "Deploy additional medical staff."

        if heat_index < 54:
            return "Restrict entry and increase cooling."

        return "Evacuate area immediately."
    
    def trend(self) -> str:

        if len(self._history) < 2:
            return "Stable"

        previous = self._history[-2]["heat_index"]
        current = self._history[-1]["heat_index"]

        if current > previous:
            return "Rising"

        if current < previous:
            return "Falling"

        return "Stable"

    # ========================================================
    # Heat Risk Score
    # ========================================================

    def risk_score(
        self,
        heat_index: float
    ) -> int:
        """
        Converts the heat index into a
        normalized risk score (0-100).
        """

        score = int(
            min(
                100,
                max(
                    0,
                    (heat_index - 20) * 3
                )
            )
        )

        return score

    # ========================================================
    # Build Reading
    # ========================================================

    def reading(
        self,
        temperature: float,
        humidity: float
    ) -> Dict:
        """
        Creates a complete heat report.
        """

        heat_index = self.calculate(
            temperature,
            humidity
        )

        report = {

            "timestamp": datetime.now().isoformat(),

            "temperature": round(temperature,2),

            "humidity": round(humidity,2),

            "heat_index": heat_index,

            "status": self.status(heat_index),

            "severity": self.severity(heat_index),

            "comfort": self.comfort(heat_index),

            "risk_score": self.risk_score(heat_index),

            "heatstroke_probability":
                self.heatstroke_probability(heat_index),

            "recommendation":
                self.recommendation(heat_index),

            "trend": "Stable"

        }

        self._history.append(report)

        self.last_reading = report

        self.maximum_heat_index = max(
            self.maximum_heat_index,
            heat_index
        )

        self.minimum_heat_index = min(
            self.minimum_heat_index,
            heat_index
        )

        self.total_heat_index += heat_index

        self.total_readings += 1

        report["trend"] = self.trend()

        return report

    def statistics(self):

        average = (
            self.total_heat_index /
            self.total_readings
            if self.total_readings
            else 0
        )

        return {

            "maximum_heat_index":
                self.maximum_heat_index,

            "minimum_heat_index":
                (
                    0
                    if self.minimum_heat_index == float("inf")
                    else self.minimum_heat_index
                ),

            "average_heat_index":
                round(average,2),

            "total_readings":
                self.total_readings,

            "latest":
                self.last_reading

        }
    
    def predict_next(self):

        if len(self._history) < 5:

            if self.last_reading:

                return self.last_reading["heat_index"]

            return 0.0

        values = [

            item["heat_index"]

            for item in list(self._history)[-5:]

        ]

        differences = [

            values[i] - values[i-1]

            for i in range(1, len(values))

        ]

        average_change = mean(differences)

        return round(

            values[-1] + average_change,

            2

        )
    
    def summary(self):

        if self.last_reading is None:
            return {}

        return {

            "heat_index":
                self.last_reading["heat_index"],

            "status":
                self.last_reading["status"],

            "severity":
                self.last_reading["severity"],

            "comfort":
                self.last_reading["comfort"],

            "risk_score":
                self.last_reading["risk_score"],

            "heatstroke_probability":
                self.last_reading["heatstroke_probability"],

            "recommendation":
                self.last_reading["recommendation"],

            "trend":
                self.last_reading["trend"]

        }
    
    def history(self):

     return list(self._history)
    
    def info(self):

        return {

            "module":
                "Heat Index Calculator",

            "status":
                "Running",

            "formula":
                self.formula,

            "history_size":
                len(self._history),

            "latest_timestamp":
                (
                    self.last_reading["timestamp"]
                    if self.last_reading
                    else None
                )

        }
    
    def reset(self):

        self._history.clear()

        self.last_reading = None

        self.maximum_heat_index = float("-inf")

        self.minimum_heat_index = float("inf")

        self.total_heat_index = 0.0

        self.total_readings = 0

    def requires_alert(
        self,
        heat_index: float
    ):

        return heat_index >= 41


# ============================================================
# Singleton
# ============================================================

heat_index_calculator = HeatIndexCalculator()