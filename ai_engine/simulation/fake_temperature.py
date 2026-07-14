"""
============================================================
Astravon Live Arena
Fake Temperature Generator

Purpose:
    Simulates environmental conditions for testing
    and development.

    Generates:
        - Temperature
        - Humidity
        - Heat Index

Author:
    House of Astravon
Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import random
from typing import Dict


class FakeTemperature:
    """
    Simulates environmental conditions.
    """

    def __init__(
        self,
        base_temperature: float = 26.0,
        base_humidity: float = 55.0
    ) -> None:

        self.base_temperature = base_temperature
        self.base_humidity = base_humidity

        self.temperature = base_temperature
        self.humidity = base_humidity

    # ========================================================
    # Temperature
    # ========================================================

    def generate(self) -> Dict:
        """
        Generates simulated environmental data.
        """

        temperature_change = random.uniform(-1.2, 1.2)
        humidity_change = random.uniform(-3.0, 3.0)

        self.temperature += temperature_change
        self.humidity += humidity_change

        self.temperature = max(18.0, min(45.0, self.temperature))
        self.humidity = max(20.0, min(95.0, self.humidity))

        heat_index = self.calculate_heat_index(
            self.temperature,
            self.humidity
        )

        return {
            "temperature": round(self.temperature, 1),
            "humidity": round(self.humidity, 1),
            "heat_index": round(heat_index, 1)
        }

    # ========================================================
    # Heat Index
    # ========================================================

    def calculate_heat_index(
        self,
        temperature: float,
        humidity: float
    ) -> float:
        """
        Simple heat index approximation.
        """

        return (
            temperature +
            (humidity / 100) * 6
        )

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Restores default values.
        """

        self.temperature = self.base_temperature
        self.humidity = self.base_humidity

    # ========================================================
    # Configuration
    # ========================================================

    def set_temperature(
        self,
        value: float
    ) -> None:
        """
        Sets the current temperature.
        """

        self.temperature = value

    def set_humidity(
        self,
        value: float
    ) -> None:
        """
        Sets the current humidity.
        """

        self.humidity = value

    # ========================================================
    # Current Values
    # ========================================================

    def current(self) -> Dict:
        """
        Returns current environmental values.
        """

        return {
            "temperature": round(self.temperature, 1),
            "humidity": round(self.humidity, 1),
            "heat_index": round(
                self.calculate_heat_index(
                    self.temperature,
                    self.humidity
                ),
                1
            )
        }


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    simulator = FakeTemperature()

    for _ in range(10):
        print(simulator.generate())