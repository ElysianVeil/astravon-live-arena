"""
============================================================
Astravon Live Arena
Risk Severity

Purpose:
    Converts numerical risk scores into
    human-readable severity levels.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import Dict

from .thresholds import RISK


class RiskSeverity:
    """
    Determines the severity of an event
    based on its overall risk score.
    """

    def __init__(self):
        self.thresholds = RISK

    # ========================================================
    # Classify Risk
    # ========================================================

    def classify(
        self,
        score: int
    ) -> str:
        """
        Returns the severity level.

        Args:
            score: Overall risk score (0-100)

        Returns:
            Severity level.
        """

        if score >= self.thresholds.CRITICAL:
            return "Critical"

        if score >= self.thresholds.HIGH:
            return "High"

        if score >= self.thresholds.MEDIUM:
            return "Medium"

        return "Low"

    # ========================================================
    # Detailed Severity
    # ========================================================

    def details(
        self,
        score: int
    ) -> Dict:
        """
        Returns complete severity information.
        """

        level = self.classify(score)

        return {
            "score": score,
            "level": level,
            "color": self.color(level),
            "description": self.description(level)
        }

    # ========================================================
    # Severity Color
    # ========================================================

    def color(
        self,
        level: str
    ) -> str:
        """
        Returns dashboard color.
        """

        colors = {
            "Low": "#2ECC71",
            "Medium": "#F1C40F",
            "High": "#E67E22",
            "Critical": "#E74C3C"
        }

        return colors.get(level, "#95A5A6")

    # ========================================================
    # Severity Description
    # ========================================================

    def description(
        self,
        level: str
    ) -> str:
        """
        Returns a human-readable description.
        """

        descriptions = {
            "Low": (
                "Conditions are safe. Continue normal monitoring."
            ),

            "Medium": (
                "Potential risks detected. Increase observation."
            ),

            "High": (
                "High risk detected. Prepare emergency response."
            ),

            "Critical": (
                "Critical danger. Immediate intervention required."
            )
        }

        return descriptions.get(
            level,
            "Unknown risk level."
        )

    # ========================================================
    # Boolean Helpers
    # ========================================================

    def is_safe(
        self,
        score: int
    ) -> bool:
        """
        Returns True if risk is low.
        """

        return self.classify(score) == "Low"

    def requires_attention(
        self,
        score: int
    ) -> bool:
        """
        Returns True if additional monitoring
        is recommended.
        """

        return self.classify(score) in (
            "Medium",
            "High",
            "Critical"
        )

    def requires_emergency_response(
        self,
        score: int
    ) -> bool:
        """
        Returns True if emergency teams
        should respond.
        """

        return self.classify(score) == "Critical"