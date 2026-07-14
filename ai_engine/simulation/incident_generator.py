"""
============================================================
Astravon Live Arena
Incident Generator

Purpose:
    Simulates incidents during an event for testing
    the AI pipeline, alert system, and dashboard.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Dict, Optional


class IncidentGenerator:
    """
    Simulates incidents occurring during an event.
    """

    def __init__(self) -> None:

        self.total_incidents = 0

        self.incident_types = [
            "Medical Emergency",
            "Overcrowding",
            "Blocked Exit",
            "Fire Alarm",
            "Suspicious Object",
            "Aggressive Behaviour",
            "Equipment Failure",
            "Heat Stress"
        ]

        self.severity_levels = [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]

    # ========================================================
    # Incident Generation
    # ========================================================

    def generate(
        self,
        people_count: int
    ) -> Optional[Dict]:
        """
        Randomly generates an incident.

        Larger crowds increase the chance of
        an incident occurring.
        """

        probability = min(
            0.02 + (people_count / 5000),
            0.60
        )

        if random.random() > probability:
            return None

        self.total_incidents += 1

        incident_type = random.choice(
            self.incident_types
        )

        severity = self._determine_severity(
            incident_type,
            people_count
        )

        return {
            "id": self.total_incidents,
            "type": incident_type,
            "severity": severity,
            "people_count": people_count,
            "location": self._random_location(),
            "description": self._description(
                incident_type
            ),
            "timestamp": datetime.now().isoformat()
        }

    # ========================================================
    # Severity
    # ========================================================

    def _determine_severity(
        self,
        incident_type: str,
        people_count: int
    ) -> str:
        """
        Determines incident severity.
        """

        if incident_type == "Fire Alarm":
            return "Critical"

        if incident_type == "Medical Emergency":
            return random.choice(
                ["Medium", "High"]
            )

        if incident_type == "Overcrowding":

            if people_count > 400:
                return "Critical"

            if people_count > 250:
                return "High"

            return "Medium"

        return random.choice(
            self.severity_levels
        )

    # ========================================================
    # Location
    # ========================================================

    def _random_location(self) -> str:
        """
        Returns a simulated location.
        """

        locations = [
            "North Entrance",
            "South Entrance",
            "East Stand",
            "West Stand",
            "VIP Section",
            "Main Gate",
            "Parking Area",
            "Food Court",
            "Emergency Exit A",
            "Emergency Exit B"
        ]

        return random.choice(locations)

    # ========================================================
    # Description
    # ========================================================

    def _description(
        self,
        incident_type: str
    ) -> str:
        """
        Generates an incident description.
        """

        descriptions = {
            "Medical Emergency":
                "A person requires immediate medical attention.",

            "Overcrowding":
                "Crowd density has exceeded the safe threshold.",

            "Blocked Exit":
                "An emergency exit appears obstructed.",

            "Fire Alarm":
                "Fire alarm activated. Immediate investigation required.",

            "Suspicious Object":
                "An unattended object has been detected.",

            "Aggressive Behaviour":
                "Potential conflict detected within the crowd.",

            "Equipment Failure":
                "Venue equipment malfunction detected.",

            "Heat Stress":
                "Environmental conditions may cause heat exhaustion."
        }

        return descriptions.get(
            incident_type,
            "Unknown incident."
        )

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Resets simulator statistics.
        """

        self.total_incidents = 0

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self) -> Dict:
        """
        Returns generator statistics.
        """

        return {
            "generated_incidents": self.total_incidents
        }


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    generator = IncidentGenerator()

    for _ in range(15):

        incident = generator.generate(
            people_count=random.randint(0, 500)
        )

        print(incident)