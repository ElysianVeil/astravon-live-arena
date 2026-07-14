"""
============================================================
Astravon Live Arena
Crowd Generator

Purpose:
    Simulates crowd statistics for testing and
    development without requiring live camera feeds.

    Generates:
        - People count
        - Crowd density
        - Venue occupancy
        - Crowd movement
        - Congestion level

Author:
    House of Astravon
Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import random
from typing import Dict


class CrowdGenerator:
    """
    Generates simulated crowd information.
    """

    def __init__(
        self,
        capacity: int = 500
    ) -> None:

        self.capacity = capacity
        self.people_count = 0

    # ========================================================
    # Crowd Generation
    # ========================================================

    def generate(self) -> Dict:
        """
        Generates one set of crowd statistics.
        """

        change = random.randint(-12, 20)

        self.people_count += change

        self.people_count = max(
            0,
            min(self.capacity, self.people_count)
        )

        occupancy = round(
            (self.people_count / self.capacity) * 100,
            1
        )

        density = self._calculate_density(
            self.people_count
        )

        movement = random.choice([
            "Stable",
            "Entering",
            "Leaving",
            "Dispersing",
            "Gathering"
        ])

        congestion = self._calculate_congestion(
            occupancy
        )

        return {
            "people_count": self.people_count,
            "capacity": self.capacity,
            "occupancy": occupancy,
            "density": density,
            "movement": movement,
            "congestion": congestion
        }

    # ========================================================
    # Density
    # ========================================================

    def _calculate_density(
        self,
        people: int
    ) -> str:

        percentage = (
            people / self.capacity
        ) * 100

        if percentage < 30:
            return "Low"

        if percentage < 60:
            return "Medium"

        if percentage < 85:
            return "High"

        return "Critical"

    # ========================================================
    # Congestion
    # ========================================================

    def _calculate_congestion(
        self,
        occupancy: float
    ) -> str:

        if occupancy < 30:
            return "Free Flow"

        if occupancy < 60:
            return "Moderate"

        if occupancy < 85:
            return "Congested"

        return "Severe"

    # ========================================================
    # Configuration
    # ========================================================

    def set_capacity(
        self,
        capacity: int
    ) -> None:
        """
        Updates venue capacity.
        """

        self.capacity = max(1, capacity)

    def set_people_count(
        self,
        people: int
    ) -> None:
        """
        Manually sets crowd size.
        """

        self.people_count = max(
            0,
            min(people, self.capacity)
        )

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Resets simulator.
        """

        self.people_count = 0

    # ========================================================
    # Current Status
    # ========================================================

    def current(self) -> Dict:
        """
        Returns current crowd information.
        """

        occupancy = round(
            (self.people_count / self.capacity) * 100,
            1
        )

        return {
            "people_count": self.people_count,
            "capacity": self.capacity,
            "occupancy": occupancy,
            "density": self._calculate_density(
                self.people_count
            ),
            "congestion": self._calculate_congestion(
                occupancy
            )
        }


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    simulator = CrowdGenerator(capacity=1000)

    for _ in range(10):
        print(simulator.generate())