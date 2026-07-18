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

        self.history = []

        self.last_level = None

        self.total_classifications = 0

        self.maximum_score = 0

        self.minimum_score = 100

        self.high_events = 0

        self.critical_events = 0

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
            level = "Critical"

        if score >= self.thresholds.HIGH:
            level = "High"

        if score >= self.thresholds.MONITOR:
            level = "Medium"

        level = "Low"

        self.history.append(level)

        self.last_level = level

        self.total_classifications += 1

        self.maximum_score = max(
            self.maximum_score,
            score
        )

        self.minimum_score = min(
            self.minimum_score,
            score
        )

        if level == "High":
            self.high_events += 1

        elif level == "Critical":
            self.critical_events += 1

        return level

    # ========================================================
    # Severity Rank
    # ========================================================

    def rank(
        self,
        level: str
    ) -> int:

        ranks = {

            "Low":1,

            "Medium":2,

            "High":3,

            "Critical":4

        }

        return ranks.get(level,0)

    # ========================================================
    # Dashboard Icon
    # ========================================================

    def icon(
        self,
        level: str
    ) -> str:

        icons = {

            "Low":"🟢",

            "Medium":"🟡",

            "High":"🟠",

            "Critical":"🔴"

        }

        return icons.get(level,"⚪")

    # ========================================================
    # Priority
    # ========================================================

    def priority(
        self,
        level:str
    ) -> str:

        priorities = {

            "Low":"Routine",

            "Medium":"Monitor",

            "High":"Urgent",

            "Critical":"Emergency"

        }

        return priorities[level]
    
    # ========================================================
    # Response Time
    # ========================================================

    def response_time(
        self,
        level:str
    )->int:

        times={

            "Low":300,

            "Medium":120,

            "High":30,

            "Critical":5

        }

        return times[level]

    # ========================================================
    # Escalation
    # ========================================================

    def escalation(
        self,
        level:str
    )->str:

        mapping={

            "Low":"None",

            "Medium":"Supervisor",

            "High":"Security",

            "Critical":"Emergency Services"

        }

        return mapping[level]

    # ========================================================
    # Alert Required
    # ========================================================

    def requires_alert(
        self,
        level:str
    )->bool:

        return level in (

            "High",

            "Critical"

        )
    
    # ========================================================
    # Evacuation
    # ========================================================

    def requires_evacuation(
        self,
        level:str
    )->bool:

        return level=="Critical"
    
    # ========================================================
    # Confidence
    # ========================================================

    def confidence(
        self,
        score:int
    )->float:

        distance=min(

            abs(score-25),

            abs(score-50),

            abs(score-75),

            abs(score-90)

        )

        confidence=max(

            50,

            100-distance

        )

        return round(confidence,1)
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

        return{

            "score":score,

            "level":level,

            "rank":self.rank(level),

            "color":self.color(level),

            "icon":self.icon(level),

            "priority":self.priority(level),

            "description":self.description(level),

            "response_time":self.response_time(level),

            "escalation":self.escalation(level),

            "confidence":self.confidence(score),

            "alert_required":self.requires_alert(level),

            "evacuation_required":self.requires_evacuation(level)

        }

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self):

        average = 0

        if self.total_classifications:

            average = (

                self.maximum_score +

                self.minimum_score

            ) / 2

        return{

            "total_classifications":self.total_classifications,

            "high_events":self.high_events,

            "critical_events":self.critical_events,

            "maximum_score":self.maximum_score,

            "minimum_score":(

                0

                if self.minimum_score==100

                else self.minimum_score

            ),

            "average_score":round(average,2),

            "last_level":self.last_level

        }

    # ========================================================
    # Summary
    # ========================================================

    def summary(
        self,
        score:int
    ):

        return self.details(score)

    # ========================================================
    # Module Info
    # ========================================================

    def info(self):

        return{

            "module":"Risk Severity",

            "status":"Running",

            "history_size":len(self.history),

            "last_level":self.last_level

        }

    # ========================================================
    # History
    # ========================================================

    def history_log(self):

        return list(self.history)

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):

        self.history.clear()

        self.last_level=None

        self.total_classifications=0

        self.maximum_score=0

        self.minimum_score=100

        self.high_events=0

        self.critical_events=0

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