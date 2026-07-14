"""
============================================================
Astravon Live Arena
Occupancy Analyzer

Purpose:
    Calculates occupancy statistics for monitored
    areas and determines whether an area is approaching
    or exceeding its capacity.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import Dict


# ============================================================
# Occupancy Analyzer
# ============================================================

class OccupancyAnalyzer:
    """
    Calculates occupancy information for a venue.
    """

    def __init__(
        self,
        maximum_capacity: int = 500
    ):
        self.maximum_capacity = maximum_capacity

    # --------------------------------------------------------

    def occupancy_percentage(
        self,
        people_count: int
    ) -> float:
        """
        Returns occupancy percentage.
        """

        if self.maximum_capacity <= 0:
            return 0.0

        percentage = (
            people_count / self.maximum_capacity
        ) * 100

        return round(percentage, 2)

    # --------------------------------------------------------

    def available_space(
        self,
        people_count: int
    ) -> int:
        """
        Returns remaining capacity.
        """

        remaining = self.maximum_capacity - people_count

        return max(remaining, 0)

    # --------------------------------------------------------

    def is_full(
        self,
        people_count: int
    ) -> bool:
        """
        Returns True if the venue is full.
        """

        return people_count >= self.maximum_capacity

    # --------------------------------------------------------

    def is_over_capacity(
        self,
        people_count: int
    ) -> bool:
        """
        Returns True if capacity is exceeded.
        """

        return people_count > self.maximum_capacity

    # --------------------------------------------------------

    def occupancy_status(
        self,
        people_count: int
    ) -> str:
        """
        Returns occupancy status.
        """

        percentage = self.occupancy_percentage(
            people_count
        )

        if percentage < 25:
            return "Mostly Empty"

        if percentage < 50:
            return "Moderately Occupied"

        if percentage < 75:
            return "Busy"

        if percentage < 100:
            return "Nearly Full"

        if percentage == 100:
            return "Full"

        return "Over Capacity"

    # --------------------------------------------------------

    def analyze(
        self,
        people_count: int
    ) -> Dict:
        """
        Returns complete occupancy information.
        """

        return {
            "people_count": people_count,
            "maximum_capacity": self.maximum_capacity,
            "occupancy_percentage": self.occupancy_percentage(
                people_count
            ),
            "available_space": self.available_space(
                people_count
            ),
            "status": self.occupancy_status(
                people_count
            ),
            "is_full": self.is_full(
                people_count
            ),
            "is_over_capacity": self.is_over_capacity(
                people_count
            )
        }

    # --------------------------------------------------------

    def update_capacity(
        self,
        capacity: int
    ):
        """
        Updates maximum venue capacity.
        """

        if capacity > 0:
            self.maximum_capacity = capacity

    # --------------------------------------------------------

    def get_capacity(self) -> int:
        """
        Returns configured capacity.
        """

        return self.maximum_capacity


# ============================================================
# Singleton Instance
# ============================================================

occupancy_analyzer = OccupancyAnalyzer()