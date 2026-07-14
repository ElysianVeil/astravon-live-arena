"""
============================================================
Astravon Live Arena
Crowd Density Analyzer

Purpose:
    Calculates crowd density levels and occupancy
    percentages from detected people counts.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import Dict


# ============================================================
# Crowd Density Analyzer
# ============================================================

class CrowdDensity:
    """
    Determines crowd density based on
    people count and venue capacity.
    """

    def __init__(
        self,
        venue_capacity: int = 500
    ):
        self.venue_capacity = venue_capacity

    # --------------------------------------------------------

    def occupancy_percentage(
        self,
        people_count: int
    ) -> float:
        """
        Calculates occupancy percentage.
        """

        if self.venue_capacity <= 0:
            return 0.0

        percentage = (
            people_count / self.venue_capacity
        ) * 100

        return round(percentage, 2)

    # --------------------------------------------------------

    def density_level(
        self,
        people_count: int
    ) -> str:
        """
        Returns crowd density level.
        """

        percentage = self.occupancy_percentage(
            people_count
        )

        if percentage < 25:
            return "Low"

        if percentage < 50:
            return "Medium"

        if percentage < 75:
            return "High"

        return "Critical"

    # --------------------------------------------------------

    def people_per_square_meter(
        self,
        people_count: int,
        area_m2: float
    ) -> float:
        """
        Calculates crowd density using
        people per square meter.
        """

        if area_m2 <= 0:
            return 0.0

        density = people_count / area_m2

        return round(
            density,
            2
        )

    # --------------------------------------------------------

    def density_status(
        self,
        people_per_m2: float
    ) -> str:
        """
        Classifies density using
        international crowd guidance.
        """

        if people_per_m2 < 1:
            return "Free Flow"

        if people_per_m2 < 2:
            return "Comfortable"

        if people_per_m2 < 3:
            return "Busy"

        if people_per_m2 < 4:
            return "Congested"

        return "Danger"

    # --------------------------------------------------------

    def analyze(
        self,
        people_count: int,
        area_m2: float = 100.0
    ) -> Dict:
        """
        Performs complete density analysis.
        """

        occupancy = self.occupancy_percentage(
            people_count
        )

        level = self.density_level(
            people_count
        )

        people_density = self.people_per_square_meter(
            people_count,
            area_m2
        )

        status = self.density_status(
            people_density
        )

        return {
            "people_count": people_count,
            "venue_capacity": self.venue_capacity,
            "occupancy_percentage": occupancy,
            "density_level": level,
            "people_per_square_meter": people_density,
            "density_status": status
        }

    # --------------------------------------------------------

    def set_capacity(
        self,
        capacity: int
    ):
        """
        Updates venue capacity.
        """

        if capacity > 0:
            self.venue_capacity = capacity

    # --------------------------------------------------------

    def get_capacity(self) -> int:
        """
        Returns venue capacity.
        """

        return self.venue_capacity


# ============================================================
# Singleton Instance
# ============================================================

density_analyzer = CrowdDensity()