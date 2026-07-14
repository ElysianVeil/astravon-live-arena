"""
============================================================
Astravon Live Arena
Temperature Manager

Purpose:
    Manages environmental temperature values for the
    AI engine. Can operate in simulation mode or later
    be connected to a real weather station or IoT sensor.

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


class TemperatureManager:
    """
    Handles temperature readings.
    """

    def __init__(
        self,
        initial_temperature: float = 25.0,
        minimum_temperature: float = 15.0,
        maximum_temperature: float = 45.0,
    ):
        self.initial_temperature = initial_temperature
        self.minimum_temperature = minimum_temperature
        self.maximum_temperature = maximum_temperature

        self.temperature = initial_temperature

    # ========================================================
    # Current Temperature
    # ========================================================

    def current(self) -> float:
        """
        Returns the current temperature.
        """

        return round(self.temperature, 2)

    # ========================================================
    # Update Temperature
    # ========================================================

    def update(
        self,
        value: float
    ) -> float:
        """
        Updates the current temperature.
        """

        value = max(
            self.minimum_temperature,
            min(
                self.maximum_temperature,
                value
            )
        )

        self.temperature = value

        return self.current()

    # ========================================================
    # Simulate Temperature
    # ========================================================

    def simulate(self) -> float:
        """
        Generates a realistic temperature change.
        """

        self.temperature += random.uniform(
            -0.5,
            0.5
        )

        self.temperature = max(
            self.minimum_temperature,
            min(
                self.maximum_temperature,
                self.temperature
            )
        )

        return self.current()

    # ========================================================
    # Temperature Status
    # ========================================================

    def status(self) -> str:
        """
        Returns a temperature classification.
        """

        temp = self.temperature

        if temp < 20:
            return "Cold"

        if temp < 28:
            return "Comfortable"

        if temp < 35:
            return "Warm"

        return "Hot"

    # ========================================================
    # Reading
    # ========================================================

    def reading(self) -> Dict:
        """
        Returns a complete temperature reading.
        """

        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": self.current(),
            "status": self.status()
        }

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):
        """
        Restores the default temperature.
        """

        self.temperature = self.initial_temperature


# ============================================================
# Singleton Instance
# ============================================================

temperature_manager = TemperatureManager()