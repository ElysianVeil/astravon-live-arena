"""
============================================================
Astravon Live Arena
Event Simulator

Purpose:
    Simulates a live event by generating crowd data,
    environmental conditions, and random incidents for
    development and testing.

Author:
    House of Astravon
Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import random
import time
from datetime import datetime
from typing import Dict

from simulation.crowd_generator import CrowdGenerator
from simulation.fake_temperature import FakeTemperature
from simulation.incident_generator import IncidentGenerator


class EventSimulator:
    """
    Simulates an event environment.

    Coordinates:
        - Crowd generation
        - Temperature simulation
        - Incident generation
    """

    def __init__(self) -> None:

        self.crowd_generator = CrowdGenerator()
        self.temperature_generator = FakeTemperature()
        self.incident_generator = IncidentGenerator()

        self.running = False

        self.event_name = "Simulation Event"

        self.tick = 0

    # ========================================================
    # Control
    # ========================================================

    def start(self) -> None:
        """
        Starts the simulator.
        """

        self.running = True
        self.tick = 0

    def stop(self) -> None:
        """
        Stops the simulator.
        """

        self.running = False

    def is_running(self) -> bool:
        """
        Returns simulator status.
        """

        return self.running

    # ========================================================
    # Configuration
    # ========================================================

    def set_event_name(
        self,
        name: str
    ) -> None:
        """
        Sets event name.
        """

        self.event_name = name

    # ========================================================
    # Simulation
    # ========================================================

    def next_frame(self) -> Dict:
        """
        Generates the next simulated frame.
        """

        if not self.running:
            raise RuntimeError(
                "Simulator is not running."
            )

        self.tick += 1

        crowd = self.crowd_generator.generate()

        temperature = self.temperature_generator.generate()

        incident = self.incident_generator.generate(
            crowd["people_count"]
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "event": self.event_name,
            "frame": self.tick,
            "crowd": crowd,
            "environment": {
                "temperature": temperature
            },
            "incident": incident
        }

    # ========================================================
    # Continuous Simulation
    # ========================================================

    def run(
        self,
        delay: float = 1.0
    ):
        """
        Generator that continuously produces
        simulated event data.
        """

        self.start()

        while self.running:

            yield self.next_frame()

            time.sleep(delay)

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:
        """
        Resets simulator state.
        """

        self.tick = 0

        self.crowd_generator.reset()

        self.temperature_generator.reset()

        self.incident_generator.reset()

    # ========================================================
    # Information
    # ========================================================

    def info(self) -> Dict:
        """
        Returns simulator information.
        """

        return {
            "event": self.event_name,
            "running": self.running,
            "frame": self.tick
        }


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    simulator = EventSimulator()

    simulator.set_event_name("Football Match")

    simulator.start()

    for _ in range(5):

        print(simulator.next_frame())

        time.sleep(1)

    simulator.stop()