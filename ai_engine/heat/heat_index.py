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


class HeatIndexCalculator:
    """
    Calculates heat index values.
    """

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

        Uses a simplified approximation suitable
        for the MVP.
        """

        heat_index = (
            temperature +
            ((humidity / 100) * 5)
        )

        return round(heat_index, 2)

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

        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "heat_index": heat_index,
            "status": self.status(heat_index),
            "risk_score": self.risk_score(heat_index)
        }


# ============================================================
# Singleton
# ============================================================

heat_index_calculator = HeatIndexCalculator()