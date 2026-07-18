"""
============================================================
Astravon Live Arena
Risk Recommendations

Purpose:
    Generates recommendations based on the
    current event risk level.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import Dict, List
from collections import deque
from datetime import datetime


class RecommendationEngine:
    """
    Generates operational recommendations
    for event managers.
    """

    def __init__(self):

        self._recommendations = {

            "Low": [

                "Continue normal monitoring.",

                "Maintain routine security patrols.",

                "Monitor crowd statistics.",

                "Keep emergency teams on standby."
            ],

            "Medium": [

                "Increase crowd monitoring.",

                "Deploy additional security personnel.",

                "Notify event supervisors.",

                "Prepare first aid stations.",

                "Monitor venue entrances and exits."
            ],

            "High": [

                "Activate emergency response team.",

                "Increase public announcements.",

                "Open additional exits if available.",

                "Restrict further entry if necessary.",

                "Deploy medical personnel.",

                "Continuously monitor crowd movement."
            ],

            "Critical": [

                "Initiate emergency evacuation procedures.",

                "Contact emergency services immediately.",

                "Stop event activities.",

                "Broadcast emergency instructions.",

                "Open every emergency exit.",

                "Direct the crowd to safe assembly areas.",

                "Dispatch all available security personnel.",

                "Monitor crowd movement continuously."
            ]
        }

        self.history = deque(maxlen=1000)

        self.last_report = None

        self.total_reports = 0

        self.total_recommendations_generated = 0

        self.alert_recommendations = 0

        self.maximum_risk_level = "Low"

    # ========================================================
    # Public API
    # ========================================================

    def generate(
        self,
        level: str,
        people_count: int,
        occupancy: float,
        density: str,
        heat_index: float,
        movement: str,
        # prediction: dict | None = None
    ) -> list[str]:
        """
        Returns recommendations for the
        specified risk level.
        """
        recommendations = list(
            self._recommendations.get(level, ["No recommendations available."])
        )

        if occupancy >= 90:

            recommendations.append(
                "Restrict additional entry."
            )

            recommendations.append(
                "Open additional exits."
            )

        if heat_index >= 41:

            recommendations.append(
                "Deploy medical teams."
            )

            recommendations.append(
                "Increase hydration stations."
            )

        if density == "High":

            recommendations.append(
                "Increase crowd dispersion."
            )

            recommendations.append(
                "Redirect pedestrian flow."
            )

        if people_count > 500:

            recommendations.append(
                "Deploy additional security."
            )

        if movement == "Busy":

            recommendations.append(
                "Investigate abnormal crowd movement."
            )

        # if prediction:

        #     if prediction["alert_required"]:

        #         recommendations.append(
        #             "Prepare emergency response."
        #         )

        #     if prediction["prediction"] == "Critical":

        #         recommendations.append(
        #             "Immediate command center review."
        #         )

        return sorted(
            set(recommendations)
        )
    
    # ========================================================
    # Recommendation Priority
    # ========================================================

    def priority(
        self,
        level: str
    ) -> str:
        priorities = {

            "Low":"Low",

            "Medium":"Medium",

            "High":"High",

            "Critical":"Immediate"

        }

        return priorities.get(level,"Unknown")
    
    def response_time(
        self,
        level:str
    )->int:
        times={

            "Low":30,

            "Medium":15,

            "High":5,

            "Critical":1

        }

        return times.get(level,30)
    
    # ========================================================
    # Required Personnel
    # ========================================================

    def personnel(
        self,
        level: str
    ) -> dict:
        """
        Returns the recommended personnel deployment.
        """

        personnel = {

            "Low": {
                "security": 4,
                "medical": 1,
                "police": 0,
                "fire": 0
            },

            "Medium": {
                "security": 8,
                "medical": 2,
                "police": 1,
                "fire": 0
            },

            "High": {
                "security": 15,
                "medical": 4,
                "police": 3,
                "fire": 1
            },

            "Critical": {
                "security": 30,
                "medical": 8,
                "police": 6,
                "fire": 2
            }

        }

        return personnel.get(
            level,
            {
                "security":0,
                "medical":0,
                "police":0,
                "fire":0
            }
        )
    
    # ========================================================
    # Emergency Actions
    # ========================================================

    def emergency_actions(
        self,
        level: str
    ) -> list[str]:
        """
        Returns emergency actions for the given level.
        """

        actions = {

            "Low":[
                "Continue Monitoring"
            ],

            "Medium":[
                "Increase Surveillance",
                "Prepare Medical Team"
            ],

            "High":[
                "Deploy Security",
                "Restrict Entry",
                "Open Additional Exits",
                "Increase Public Announcements"
            ],

            "Critical":[
                "Evacuate",
                "Contact Police",
                "Contact Ambulance",
                "Open Exits",
                "Stop Event",
                "Activate Incident Command",
                "Notify Fire Department"
            ]

        }

        return actions.get(level, [])

    # ========================================================
    # Detailed Recommendation Report
    # ========================================================

    def report(
        self,
        level: str
    ) -> Dict:
        """
        Returns a structured recommendation report.
        """

        recommendations = self.generate(level)

        report = {

            "risk_level": level,

            "recommendation_count": len(
                recommendations
            ),

            "recommendations": recommendations

        }

        report["priority"] = self.priority(level)

        report["estimated_response_minutes"] = (
            self.response_time(level)
        )

        report["personnel"] = self.personnel(level)

        report["emergency_actions"] = (
            self.emergency_actions(level)
        )

        report["generated_at"] = (
            datetime.now().isoformat()
        )

        self.history.append(report)

        self.last_report = report

        self.total_reports += 1

        self.total_recommendations_generated += len(
            recommendations
        )

        if level in ("High", "Critical"):

            self.alert_recommendations += 1

        self.maximum_risk_level = level

        return report
    
    # ========================================================
    # Recommendation Summary
    # ========================================================

    def summary(self) -> dict:
        """
        Returns the latest recommendation summary.
        """

        if self.last_report is None:

            return {}

        return {

            "last_level":
                self.last_report["risk_level"],

            "priority":
                self.last_report["priority"],

            "recommendation_count":
                self.last_report[
                    "recommendation_count"
                ],

            "estimated_response":
                self.last_report[
                    "estimated_response_minutes"
                ],

            "personnel":
                self.last_report["personnel"]

        }

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):
        """
        Recommendation engine statistics.
        """

        return {

            "reports":
                self.total_reports,

            "recommendations_generated":
                self.total_recommendations_generated,

            "alert_recommendations":
                self.alert_recommendations,

            "history_size":
                len(self.history),

            "latest":
                self.last_report

        }

    # ========================================================
    # Module Information
    # ========================================================

    def info(self):
        """
        Returns module information.
        """

        return {

            "module":
                "Recommendation Engine",

            "status":
                "Running",

            "history_size":
                len(self.history),

            "supported_levels":
                len(self._recommendations),

            "reports_generated":
                self.total_reports

        }

    def recommendation_history(self):

        return list(self.history)
    
    def reset(self):

        self.history.clear()

        self.last_report=None

        self.total_reports=0

        self.total_recommendations_generated=0

        self.alert_recommendations=0

        self.maximum_risk_level="Low"

    # ========================================================
    # Dashboard
    # ========================================================

    def dashboard(self):
        """
        Dashboard payload.
        """

        if self.last_report is None:

            return {}

        return {

            "priority":
                self.last_report["priority"],

            "recommendations":
                self.last_report[
                    "recommendations"
                ],

            "response_minutes":
                self.last_report[
                    "estimated_response_minutes"
                ],

            "personnel":
                self.last_report["personnel"],

            "emergency_actions":
                self.last_report[
                    "emergency_actions"
                ]

        }
    
    # ========================================================
    # Categorized Recommendations
    # ========================================================

    def categorized(
        self,
        recommendations: list[str]
    ):
        """
        Groups recommendations.
        """

        categories = {

            "Security": [],

            "Medical": [],

            "Operations": [],

            "Communication": []

        }

        for item in recommendations:

            text = item.lower()

            if any(
                word in text
                for word in [
                    "security",
                    "police",
                    "entry",
                    "exit"
                ]
            ):

                categories["Security"].append(item)

            elif any(
                word in text
                for word in [
                    "medical",
                    "ambulance",
                    "hydration",
                    "first aid"
                ]
            ):

                categories["Medical"].append(item)

            elif any(
                word in text
                for word in [
                    "evacuate",
                    "monitor",
                    "deploy",
                    "stop"
                ]
            ):

                categories["Operations"].append(item)

            else:

                categories["Communication"].append(item)

        return categories
    
    # ========================================================
    # Action Checklist
    # ========================================================

    def checklist(
        self,
        level: str
    ) -> list[dict]:
        """
        Returns an operational checklist.
        """

        checklist = []

        for recommendation in self.generate(level):

            priority = level

            if "Evacuate" in recommendation:

                priority = "Critical"

            elif "Deploy" in recommendation:

                priority = "High"

            elif "Monitor" in recommendation:

                priority = "Medium"

            checklist.append(

                {

                    "task":
                        recommendation,

                    "completed":
                        False,

                    "priority":
                        priority

                }

            )

        return checklist

    # ========================================================
    # Utility
    # ========================================================

    def available_levels(self) -> List[str]:
        """
        Returns supported risk levels.
        """

        return list(
            self._recommendations.keys()
        )

    # ========================================================
    # Add Recommendation
    # ========================================================

    def add(
        self,
        level: str,
        recommendation: str
    ) -> None:
        """
        Adds a recommendation to a level.
        """

        if level not in self._recommendations:

            self._recommendations[level] = []

        self._recommendations[level].append(
            recommendation
        )

    # ========================================================
    # Remove Recommendation
    # ========================================================

    def remove(
        self,
        level: str,
        recommendation: str
    ) -> bool:
        """
        Removes a recommendation.

        Returns True if removed.
        """

        if (
            level in self._recommendations and
            recommendation in self._recommendations[level]
        ):

            self._recommendations[level].remove(
                recommendation
            )

            return True

        return False

    # ========================================================
    # Clear Level
    # ========================================================

    def clear(
        self,
        level: str
    ) -> None:
        """
        Removes all recommendations
        for one risk level.
        """

        if level in self._recommendations:

            self._recommendations[level].clear()