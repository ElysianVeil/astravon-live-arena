"""
============================================================
Astravon Live Arena
Heat Alert Manager

Purpose:
    Generates heat-related alerts based on
    temperature, humidity and heat index.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import Dict, List

from .heat_index import HeatIndexCalculator


class HeatAlertManager:
    """
    Generates heat alerts.

    Uses the calculated heat index to determine
    the severity of environmental conditions.
    """

    def __init__(self):
        self.heat_index = HeatIndexCalculator()
        self.alert_history: List[Dict] = []

    # ========================================================
    # Create Alert
    # ========================================================

    def evaluate(
        self,
        temperature: float,
        humidity: float
    ) -> Dict:
        """
        Evaluate current environmental conditions.
        """

        heat_index = self.heat_index.calculate(
            temperature,
            humidity
        )

        if heat_index >= 54:
            severity = "Critical"
            message = (
                "Extreme heat danger. Immediate evacuation "
                "or cooling intervention recommended."
            )

        elif heat_index >= 41:
            severity = "High"
            message = (
                "Dangerous heat conditions detected."
            )

        elif heat_index >= 32:
            severity = "Medium"
            message = (
                "High heat stress. Monitor the crowd closely."
            )

        elif heat_index >= 27:
            severity = "Low"
            message = (
                "Warm conditions detected."
            )

        else:
            severity = "Safe"
            message = (
                "Environmental conditions are normal."
            )

        alert = {
            "type": "Heat",
            "severity": severity,
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "heat_index": round(heat_index, 1),
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        self.alert_history.append(alert)

        return alert

    # ========================================================
    # Latest Alert
    # ========================================================

    def latest(self) -> Dict | None:
        """
        Returns the latest generated alert.
        """

        if not self.alert_history:
            return None

        return self.alert_history[-1]

    # ========================================================
    # Alert History
    # ========================================================

    def history(self) -> List[Dict]:
        """
        Returns all generated alerts.
        """

        return self.alert_history

    # ========================================================
    # Critical Check
    # ========================================================

    def has_critical_alert(self) -> bool:
        """
        Returns True if the latest alert is critical.
        """

        latest = self.latest()

        if latest is None:
            return False

        return latest["severity"] == "Critical"

    # ========================================================
    # Clear History
    # ========================================================

    def clear(self):
        """
        Clears alert history.
        """

        self.alert_history.clear()