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
from config import settings
from collections import deque
from utils.logger import get_logger

logger = get_logger("Occupancy Analyzer")

# ============================================================
# Occupancy Analyzer
# ============================================================

class OccupancyAnalyzer:
    """
    Calculates occupancy information for a venue.
    """

    def __init__(
        self,
        maximum_capacity=settings.VENUE_CAPACITY
    ):
        self.maximum_capacity = maximum_capacity
        self.history = deque(maxlen=300)
        self.peak_occupancy = 0.0
        self.minimum_occupancy = 100.0
        self.last_people_count = 0
        self.current_percentage = 0.0
        self.current_people_count = 0
        self.current_available_space = maximum_capacity
        self.current_status = "Mostly Empty"
        self.current_alert = None
        self.current_risk = "LOW"
        self.current_eta = None

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

        if percentage < settings.OCCUPANCY_EMPTY:
            return "Mostly Empty"

        if percentage < settings.OCCUPANCY_MODERATE:
            return "Moderately Occupied"

        if percentage < settings.OCCUPANCY_BUSY:
            return "Busy"

        if percentage < settings.OCCUPANCY_NEAR_FULL:
            return "Nearly Full"

        if percentage == settings.OCCUPANCY_FULL:
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

        self.history.append(
            self.occupancy_percentage(people_count)
        )
        percentage = self.occupancy_percentage(
            people_count
        )

        self.peak_occupancy = max(
            self.peak_occupancy,
            percentage
        )

        self.minimum_occupancy = min(
            self.minimum_occupancy,
            percentage
        )

        status = self.occupancy_status(
            people_count
        )

        alert = self.occupancy_alert(
            percentage
        )

        risk = self.risk_level(
            percentage
        )

        rate = people_count - self.last_people_count

        growth_rate = max(rate, 0)

        eta = self.estimated_time_until_full(
            growth_rate
        )

        self.last_people_count = people_count

        self.current_people_count = people_count
        self.current_percentage = percentage
        self.current_available_space = self.available_space(people_count)
        self.current_status = status
        self.current_alert = alert
        self.current_risk = risk
        self.current_eta = eta

        return {
            "people_count": people_count,
            "maximum_capacity": self.maximum_capacity,
            "occupancy_percentage": percentage,
            "available_space": self.available_space(
                people_count
            ),
            "occupied_space": people_count,

            "utilization": percentage,

            "status": status,

            "trend": self.occupancy_trend(),

            "risk_level": risk,

            "alert": alert,

            "peak_occupancy": self.peak_occupancy,

            "average_occupancy": self.average_occupancy(),

            "occupancy_change": rate,

            "estimated_time_until_full": eta,

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
    
    def average_occupancy(self):

        if not self.history:
            return 0.0

        return round(

            sum(self.history)

            /

            len(self.history),

            2

        )
    
    def occupancy_trend(self):

        if len(self.history) < 2:
            return "Stable"

        previous = self.history[-2]
        current = self.history[-1]

        if current > previous:
            return "Increasing"

        if current < previous:
            return "Decreasing"

        return "Stable"
    
    # --------------------------------------------------------

    def estimated_time_until_full(
        self,
        growth_rate: float
    ):
        """
        Estimates the time (seconds) until the venue
        reaches maximum capacity.

        growth_rate:
            People entering per second.

        Returns:
            float | None
        """

        if growth_rate <= 0:
            return None

        remaining = self.maximum_capacity - self.last_people_count

        if remaining <= 0:
            return 0

        return round(
            remaining / growth_rate,
            2
        )
        
    # --------------------------------------------------------

    def occupancy_alert(
        self,
        percentage: float
    ):
        """
        Returns occupancy alert level.
        """

        if percentage < settings.OCCUPANCY_BUSY:
            return None

        if percentage < settings.OCCUPANCY_NEAR_FULL:
            return "Busy"

        if percentage < settings.OCCUPANCY_FULL:
            return "Warning"

        return "Critical"
    
    # --------------------------------------------------------

    def risk_level(
        self,
        percentage: float
    ):
        """
        Returns occupancy risk level.
        """

        if percentage < 50:
            return "LOW"

        elif percentage < 75:
            return "MEDIUM"

        elif percentage < 90:
            return "HIGH"

        return "CRITICAL"

    def summary(self):
        """
        Returns occupancy summary statistics.
        """

        return {

            "capacity": self.maximum_capacity,

            "people_count": self.current_people_count,

            "occupancy_percentage": self.current_percentage,

            "available_space": self.current_available_space,

            "status": self.current_status,

            "alert": self.current_alert,

            "risk_level": self.current_risk,

            "estimated_time_until_full": self.current_eta,

            "peak_occupancy": self.peak_occupancy,

            "minimum_occupancy": self.minimum_occupancy,

            "average_occupancy": self.average_occupancy(),

            "trend": self.occupancy_trend()

        }

    def reset(self):

        self.history.clear()

        self.peak_occupancy = 0.0

        self.minimum_occupancy = 100.0

        self.last_people_count = 0
        
        logger.info("Occupancy analyzer reset.")



# ============================================================
# Singleton Instance
# ============================================================

occupancy_analyzer = OccupancyAnalyzer()