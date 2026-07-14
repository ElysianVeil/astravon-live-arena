"""
============================================================
Astravon Live Arena
Humidity Manager

Purpose:
    Manages environmental humidity values for the AI
    engine. Supports both simulation mode and future
    integration with real IoT sensors or weather APIs.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Dict


class HumidityManager:
    """
    Handles humidity readings.
    """

    def __init__(
        self,
        initial_humidity: float = 55.0,
        minimum_humidity: float = 20.0,
        maximum_humidity: float = 100.0,
    ):
        self.initial_humidity = initial_humidity
        self.minimum_humidity = minimum_humidity
        self.maximum_humidity = maximum_humidity

        self.humidity = initial_humidity

    # ========================================================
    # Current Humidity
    # ========================================================

    def current(self) -> float:
        """
        Returns the current humidity.
        """

        return round(self.humidity, 2)

    # ========================================================
    # Update Humidity
    # ========================================================

    def update(
        self,
        value: float
    ) -> float:
        """
        Updates the humidity value.
        """

        value = max(
            self.minimum_humidity,
            min(
                self.maximum_humidity,
                value
            )
        )

        self.humidity = value

        return self.current()

    # ========================================================
    # Simulate Humidity
    # ========================================================

    def simulate(self) -> float:
        """
        Generates realistic humidity fluctuations.
        """

        self.humidity += random.uniform(
            -2.0,
            2.0
        )

        self.humidity = max(
            self.minimum_humidity,
            min(
                self.maximum_humidity,
                self.humidity
            )
        )

        return self.current()

    # ========================================================
    # Humidity Status
    # ========================================================

    def status(self) -> str:
        """
        Returns a humidity classification.
        """

        humidity = self.humidity

        if humidity < 30:
            return "Dry"

        if humidity < 60:
            return "Comfortable"

        if humidity < 80:
            return "Humid"

        return "Very Humid"

    # ========================================================
    # Reading
    # ========================================================

    def reading(self) -> Dict:
        """
        Returns a complete humidity reading.
        """

        return {
            "timestamp": datetime.now().isoformat(),
            "humidity": self.current(),
            "status": self.status()
        }

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):
        """
        Restores the default humidity level.
        """

        self.humidity = self.initial_humidity


# ============================================================
# Singleton Instance
# ============================================================

humidity_manager = HumidityManager()