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
        self._history = []

        self.last_alert = None

        self.total_alerts = 0

        self.safe_alerts = 0

        self.low_alerts = 0

        self.medium_alerts = 0

        self.high_alerts = 0

        self.critical_alerts = 0

        self.maximum_heat_index = 0

        self.minimum_heat_index = float("inf")

        self.total_heat_index = 0

        self.alert_enabled = True

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

        heat = self.heat_index.reading(
            temperature,
            humidity
        )

        heat_index = heat["heat_index"]

        severity = heat["severity"]

        probability = heat["heatstroke_probability"]

        recommendation = heat["recommendation"]

        comfort = heat["comfort"]

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

            "type":"Heat",

            "severity":severity,

            "temperature":round(temperature,1),

            "humidity":round(humidity,1),

            "heat_index":heat_index,

            "comfort":comfort,

            "heatstroke_probability":probability,

            "recommendation":recommendation,

            "requires_medical":severity in (
                "High",
                "Critical"
            ),

            "requires_evacuation":(
                severity=="Critical"
            ),

            "messsage": message,

            "timestamp":datetime.now().isoformat()

        }

        self._history.append(alert)

        self.last_alert = alert

        self.total_alerts += 1

        self.maximum_heat_index = max(
            self.maximum_heat_index,
            heat_index
        )

        self.minimum_heat_index = min(
            self.minimum_heat_index,
            heat_index
        )

        self.total_heat_index += heat_index

        if severity=="Safe":

            self.safe_alerts +=1

        elif severity=="Low":

            self.low_alerts +=1

        elif severity=="Medium":

            self.medium_alerts +=1

        elif severity=="High":

            self.high_alerts +=1

        else:

            self.critical_alerts +=1

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
    # Alert Priority
    # ========================================================

    def priority(
        self,
        severity:str
    )->str:

        mapping={

            "Safe":"None",

            "Low":"Low",

            "Medium":"Medium",

            "High":"High",

            "Critical":"Critical"

        }

        return mapping.get(
            severity,
            "Unknown"
        )

    # ========================================================
    # Response Time
    # ========================================================

    def response_time(
        self,
        severity:str
    )->int:

        mapping={

            "Safe":60,

            "Low":30,

            "Medium":15,

            "High":5,

            "Critical":1

        }

        return mapping.get(
            severity,
            60
        )

    # ========================================================
    # Personnel
    # ========================================================

    def personnel(
        self,
        severity:str
    ):

        table={

            "Safe":{
                "medical":0,
                "security":1
            },

            "Low":{
                "medical":1,
                "security":2
            },

            "Medium":{
                "medical":2,
                "security":4
            },

            "High":{
                "medical":5,
                "security":8
            },

            "Critical":{
                "medical":10,
                "security":15
            }

        }

        return table.get(severity,{})

    # ========================================================
    # Requires Alert
    # ========================================================

    def requires_alert(
        self,
        heat_index:float
    )->bool:

        return heat_index>=41

    # ========================================================
    # Dashboard
    # ========================================================

    def dashboard(self):

        if self.last_alert is None:

            return {}

        return{

            "severity":
                self.last_alert["severity"],

            "heat_index":
                self.last_alert["heat_index"],

            "comfort":
                self.last_alert["comfort"],

            "probability":
                self.last_alert[
                    "heatstroke_probability"
                ],

            "recommendation":
                self.last_alert[
                    "recommendation"
                ],

            "response_minutes":
                self.response_time(

                    self.last_alert["severity"]

                ),

            "personnel":

                self.personnel(

                    self.last_alert["severity"]

                )

        }

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):

        average=0

        if self.total_alerts>0:

            average=round(

                self.total_heat_index

                /

                self.total_alerts,

                2

            )

        return{

            "alerts":self.total_alerts,

            "safe":self.safe_alerts,

            "low":self.low_alerts,

            "medium":self.medium_alerts,

            "high":self.high_alerts,

            "critical":self.critical_alerts,

            "maximum_heat_index":
                self.maximum_heat_index,

            "minimum_heat_index":(

                0

                if self.minimum_heat_index==float("inf")

                else self.minimum_heat_index

            ),

            "average_heat_index":
                average,

            "latest":
                self.last_alert

        }

    # ========================================================
    # Summary
    # ========================================================

    def summary(self):

        return self.last_alert or {}
    
    # ========================================================
    # Module Information
    # ========================================================

    def info(self):

        return{

            "module":
                "Heat Alert Manager",

            "status":
                "Running"

                if self.alert_enabled

                else "Disabled",

            "history_size":
                len(self.history),

            "total_alerts":
                self.total_alerts

        }
    # ========================================================
    # Alert History
    # ========================================================

    def history(self) -> List[Dict]:
        """
        Returns all generated alerts.
        """

        return list(self._history)

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

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):

        self.history.clear()

        self.last_alert=None

        self.total_alerts=0

        self.safe_alerts=0

        self.low_alerts=0

        self.medium_alerts=0

        self.high_alerts=0

        self.critical_alerts=0

        self.maximum_heat_index=0

        self.minimum_heat_index=float("inf")

        self.total_heat_index=0

    # ========================================================
    # Enable Alerts
    # ========================================================

    def enable(self):

        self.alert_enabled=True


    # ========================================================
    # Disable Alerts
    # ========================================================

    def disable(self):

        self.alert_enabled=False