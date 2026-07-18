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

from __future__ import annotations

import time
from collections import deque
from statistics import mean
from typing import Deque, Dict

from config import settings
from constants import (COLOR_GREEN, COLOR_YELLOW, COLOR_ORANGE, COLOR_RED)
from utils.logger import get_logger

logger = get_logger("CrowdDensity")

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
        venue_capacity: int = settings.VENUE_CAPACITY,
        area_m2: float = settings.VENUE_AREA
    ):

        self.venue_capacity = venue_capacity

        self.area_m2 = area_m2

        self.history: Deque[Dict] = deque(maxlen=500)

        self.maximum_density = 0

        self.maximum_people = 0

        self.frames_processed = 0

        self.total_occupancy = 0

        self.total_density = 0

        self.start_time = time.time()

        logger.info("Crowd Density Analyzer initialized.")

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
            return "Safe"

        if people_per_m2 < 2:
            return "Normal"

        if people_per_m2 < 3:
            return "Busy"

        if people_per_m2 < 4:
            return "Crowded"

        elif people_per_m2 < 5:

            return "Danger"

        return "Critical"

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

        self.frames_processed += 1

        self.total_occupancy += occupancy

        self.total_density += people_density

        self.maximum_people = max(
            self.maximum_people,
            people_count
        )

        self.maximum_density = max(
            self.maximum_density,
            people_density
        )

        self.history.append({

            "timestamp": time.time(),

            "people": people_count,

            "occupancy": occupancy,

            "density": people_density,

            "level": level,

            "status": status

        })

        return {

            "people_count":
                people_count,

            "venue_capacity":
                self.venue_capacity,

            "occupancy_percentage":
                occupancy,

            "density_level":
                level,

            "people_per_square_meter":
                people_density,

            "density_status":
                status,

            "risk_score":
                self.risk_score(
                    people_density,
                    occupancy
                ),

            "trend":
                self.trend(),

            "average_density":
                self.average_density(),

            "average_occupancy":
                self.average_occupancy()

        }
    
    def average_occupancy(self):

        if self.frames_processed == 0:
            return 0

        return round(

            self.total_occupancy /

            self.frames_processed,

            2

        )
    
    def risk_score(

        self,

        density,

        occupancy

    ):

        score = (

            density * 20 +

            occupancy * 0.6

        )

        return min(

            round(score),

            100

        )
    
    def average_density(self):

        if self.frames_processed == 0:
            return 0

        return round(

            self.total_density /

            self.frames_processed,

            2

        )
    
    def rolling_density(

        self,

        window=30

    ):

        if not self.history:
            return 0

        values = [

            x["density"]

            for x in list(self.history)[-window:]

        ]

        return round(

            mean(values),

            2

        )
    
    def trend(self):

        if len(self.history) < 2:
            return "Stable"

        previous = self.history[-2]["density"]

        current = self.history[-1]["density"]

        if current > previous:
            return "Increasing"

        elif current < previous:
            return "Decreasing"

        return "Stable"
    
    def pressure(

        self,

        people_density,

        average_speed

    ):

        pressure = (

            people_density *

            average_speed

        )

        return round(

            pressure,

            2

        )
    
    def evacuation_time(

        self,

        exits,

        people_per_second

    ):

        if exits <= 0:

            return None

        rate = exits * people_per_second

        return round(

            self.maximum_people /

            rate,

            1

        )
    
    def color(self, density):

        if density < 1:

            return COLOR_GREEN

        elif density < 2:

            return COLOR_YELLOW

        elif density < 3:

            return COLOR_ORANGE

        return COLOR_RED

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
    
    def statistics(self):

        return {

            "frames_processed":
                self.frames_processed,

            "maximum_people":
                self.maximum_people,

            "maximum_density":
                self.maximum_density,

            "average_density":
                self.average_density(),

            "average_occupancy":
                self.average_occupancy(),

            "rolling_density":
                self.rolling_density(),

            "trend":
                self.trend()

        }
    
    def reset(self):
        self.history.clear()

        self.maximum_people = 0

        self.maximum_density = 0

        self.frames_processed = 0

        self.total_density = 0

        self.total_occupancy = 0

        self.start_time = time.time()


# ============================================================
# Singleton Instance
# ============================================================

density_analyzer = CrowdDensity()