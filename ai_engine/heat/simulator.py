"""
============================================================
Astravon Live Arena
Heat Simulator

Purpose:
    Simulates environmental conditions including
    temperature and humidity for crowd safety analysis.

    This module is intended for the MVP and can later
    be replaced with real weather stations or IoT sensors.

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


class HeatSimulator:
    """
    Simulates environmental conditions.
    """

    def __init__(
        self,
        base_temperature: float = 25.0,
        base_humidity: float = 55.0
    ):
        self.base_temperature = base_temperature
        self.base_humidity = base_humidity

        self.temperature = base_temperature
        self.humidity = base_humidity

    # ========================================================
    # Temperature
    # ========================================================

    def simulate_temperature(self) -> float:
        """
        Simulates gradual temperature changes.
        """

        self.temperature += random.uniform(-0.4, 0.4)

        self.temperature = max(
            18.0,
            min(42.0, self.temperature)
        )

        return round(self.temperature, 1)

    # ========================================================
    # Humidity
    # ========================================================

    def simulate_humidity(self) -> float:
        """
        Simulates humidity changes.
        """

        self.humidity += random.uniform(-1.5, 1.5)

        self.humidity = max(
            20.0,
            min(95.0, self.humidity)
        )

        return round(self.humidity, 1)

    # ========================================================
    # Heat Index
    # ========================================================

    def calculate_heat_index(
        self,
        temperature: float,
        humidity: float
    ) -> float:
        """
        Simplified heat index calculation.
        """

        heat_index = (
            temperature +
            (humidity / 100) * 5
        )

        return round(heat_index, 1)

    # ========================================================
    # Environment
    # ========================================================

    def simulate(self) -> Dict:
        """
        Generates one environmental reading.
        """

        temperature = self.simulate_temperature()

        humidity = self.simulate_humidity()

        heat_index = self.calculate_heat_index(
            temperature,
            humidity
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "temperature": temperature,
            "humidity": humidity,
            "heat_index": heat_index
        }

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):
        """
        Restores default conditions.
        """

        self.temperature = self.base_temperature
        self.humidity = self.base_humidity


# ============================================================
# Singleton
# ============================================================

heat_simulator = HeatSimulator()