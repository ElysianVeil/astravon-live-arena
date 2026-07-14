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

    # ========================================================
    # Public API
    # ========================================================

    def generate(
        self,
        level: str
    ) -> List[str]:
        """
        Returns recommendations for the
        specified risk level.
        """

        return self._recommendations.get(
            level,
            ["No recommendations available."]
        )

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

        return {

            "risk_level": level,

            "recommendation_count": len(recommendations),

            "recommendations": recommendations
        }

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