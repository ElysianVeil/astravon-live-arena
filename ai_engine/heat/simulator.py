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
from collections import deque
from .heat_index import heat_index_calculator
import time


class HeatSimulator:
    """
    Simulates environmental conditions.
    """

    def __init__(
        self,
        base_temperature: float = 25.0,
        base_humidity: float = 55.0
    ):

        self._history = deque(maxlen=1000)

        self.last_reading = None

        self.maximum_temperature = base_temperature
        self.minimum_temperature = base_temperature

        self.maximum_humidity = base_humidity
        self.minimum_humidity = base_humidity

        self.maximum_heat_index = float("-inf")
        self.minimum_heat_index = float("inf")

        self.total_temperature = 0.0

        self.total_humidity = 0.0

        self.total_readings = 0

        self.total_heat_index = 0.0

        self.weather_code = 0

        self.weather_description = "Clear Sky"

        self.wind_speed = 4.0

        self.pressure = 1013.2

        self.uv_index = 3.0

        self.rain_probability = 0.0

        self.simulation_speed = 1.0

        self.running = True

        self.emergency = False

    # ========================================================
    # Temperature
    # ========================================================

    def simulate_temperature(self) -> float:
        """
        Simulates gradual temperature changes.
        """

        hour = datetime.now().hour

        if 5 <= hour < 12:
            drift = 0.15

        elif 12 <= hour < 16:
            drift = 0.30

        elif 16 <= hour < 20:
            drift = -0.20

        else:
            drift = -0.35

        noise = random.uniform(-0.15,0.15) * self.simulation_speed

        self.temperature += drift + noise

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

        if self.temperature > 34:

            self.humidity -= random.uniform(0.4,1.2) * self.simulation_speed

        else:

            self.humidity += random.uniform(-0.5,0.6) * self.simulation_speed

        return round(self.humidity, 1)
    
    def simulate_wind_speed(self):
        self.wind_speed += random.uniform(-0.6,0.6) * self.simulation_speed

        self.wind_speed = max(
            0,
            min(
                40,
                self.wind_speed
            )
        )

        return round(self.wind_speed, 1)
    
    def simulate_pressure(self):

        self.pressure += random.uniform(-0.5,0.5) * self.simulation_speed

        self.pressure = max(
            995,
            min(
                1035,
                self.pressure
            )
        )

        return round(self.pressure,1)
    
    def simulate_uv_index(self):

        hour = datetime.now().hour

        if 6 <= hour < 9:
            self.uv_index = 2

        elif 9 <= hour < 12:
            self.uv_index = 5

        elif 12 <= hour < 15:
            self.uv_index = 9

        elif 15 <= hour < 18:
            self.uv_index = 4

        else:
            self.uv_index = 0

        return self.uv_index
    
    def simulate_rain_probability(self):

        probability = (

            self.humidity * 0.6 +

            (1035 - self.pressure) * 1.4 +

            max(
                0,
                self.temperature - 25
            ) * 0.5

        )

        probability = max(
            0,
            min(
                100,
                probability
            )
        )

        return round(probability,1)
    
    def simulate_weather_code(self):

        rain = self.simulate_rain_probability()

        if rain > 90:

            return 95

        if rain > 70:

            return 61

        if self.humidity > 90:

            return 45

        if self.humidity > 75:

            return 3

        if self.humidity > 60:

            return 2

        if self.humidity > 40:

            return 1

        return 0
    
    def weather_description(self, code):

        mapping = {

            0:"Clear Sky",

            1:"Mainly Clear",

            2:"Partly Cloudy",

            3:"Overcast",

            45:"Fog",

            61:"Rain",

            71:"Snow",

            95:"Thunderstorm"

        }

        return mapping.get(
            code,
            "Unknown"
        )

    # ========================================================
    # Heat Index
    # ========================================================

    # def calculate_heat_index(
    #     self,
    #     temperature: float,
    #     humidity: float
    # ) -> float:
    #     """
    #     Simplified heat index calculation.
    #     """

    #     heat_index = (
    #         temperature +
    #         (humidity / 100) * 5
    #     )

    #     return round(heat_index, 1)

    # ========================================================
    # Environment
    # ========================================================

    def simulate(self) -> Dict:
        """
        Generates one environmental reading.
        """

        temperature = self.simulate_temperature()

        humidity = self.simulate_humidity()

        wind = self.simulate_wind_speed()

        pressure = self.simulate_pressure()

        uv = self.simulate_uv_index()

        rain = self.simulate_rain_probability()

        code = self.simulate_weather_code()

        description = self.weather_description(code)

        heat = heat_index_calculator.reading(
            temperature,
            humidity
        )

        reading = {
            "timestamp": datetime.now().isoformat(),
            "temperature": temperature,
            "humidity": humidity,
            "heat_index":heat["heat_index"],

            "status":heat["status"],

            "severity":heat["severity"],

            "comfort":heat["comfort"],

            "wind_speed":wind,

            "pressure":pressure,

            "uv_index":uv,

            "rain_probability":rain,

            "weather_code":code,

            "weather":description

        }

        self._history.append(reading)

        self.last_reading = reading

        self.total_readings += 1

        self.maximum_temperature = max(

            self.maximum_temperature,

            temperature

        )

        self.minimum_temperature = min(

            self.minimum_temperature,

            temperature

        )

        self.maximum_humidity = max(

            self.maximum_humidity,

            humidity

        )

        self.minimum_humidity = min(

            self.minimum_humidity,

            humidity

        )

        self.maximum_heat_index = max(

            self.maximum_heat_index,

            heat["heat_index"]

        )

        self.minimum_heat_index = min(

            self.minimum_heat_index,

            heat["heat_index"]

        )

        self.total_temperature += temperature

        self.total_humidity += humidity

        self.total_heat_index += heat["heat_index"]

        return reading

    def environment_status(self):

        heat = self.last_reading["heat_index"]

        if heat < 28:
            return "Excellent"

        elif heat < 33:
            return "Normal"

        elif heat < 38:
            return "Warm"

        elif heat < 43:
            return "Hot"

        return "Dangerous"

    def trend(self):

        if len(self._history) < 5:

            return "Stable"

        first = self._history[-5]["temperature"]

        last = self._history[-1]["temperature"]

        delta = last - first

        if delta > 1:

            return "Heating"

        elif delta < -1:

            return "Cooling"

        return "Stable"
    
    def forecast(self):

        if not self.last_reading:

            return {}

        return {

            "temperature":

                round(
                    self.temperature + random.uniform(-0.5,0.5) * self.simulation_speed,
                    1
                ),

            "humidity":

                round(
                    self.humidity + random.uniform(-1,1) * self.simulation_speed,
                    1
                ),

            "heat_index":

                round(
                    self.last_reading["heat_index"] + random.uniform(-0.5,0.5) * self.simulation_speed,
                    1
                ),

            "weather":

                self.last_reading["weather"]

        }
    
    def statistics(self):

        if self.total_readings == 0:

            return {}

        return {

            "maximum_temperature":

                self.maximum_temperature,

            "minimum_temperature":

                self.minimum_temperature,

            "average_temperature":

                round(

                    self.total_temperature /

                    self.total_readings,

                    2

                ),

            "maximum_humidity":

                self.maximum_humidity,

            "minimum_humidity":

                self.minimum_humidity,

            "average_humidity":

                round(

                    self.total_humidity /

                    self.total_readings,

                    2

                ),

            "maximum_heat_index":

                self.maximum_heat_index,

            "minimum_heat_index":

                self.minimum_heat_index,

            "average_heat_index":

                round(

                    self.total_heat_index /

                    self.total_readings,

                    2

                ),

            "total_readings":

                self.total_readings

        }
    
    def summary(self):

        if not self.last_reading:

            return {}

        return {

            **self.last_reading,

            "status":

                self.environment_status(),

            "trend":

                self.trend()

        }
    
    def info(self):

        return {

            "module":"Heat Simulator",

            "status":"Running",

            "history_size":

                len(self._history),

            "simulation_speed":

                self.simulation_speed,

            "latest_timestamp":

                self.last_reading["timestamp"]

                if self.last_reading

                else None

        }
    
    def history(self):

        return list(self._history)
    
    def set_speed(
        self,
        speed: float
    ):

        self.simulation_speed = max(
            0.5,
            min(
                10,
                speed
            )
        )

    def load_preset(
        self,
        preset
    ):

        presets = {

            "Concert":

                (31,72,8),

            "Football Match":

                (28,60,10),

            "Basketball":

                (26,55,5),

            "Festival":

                (34,78,6),

            "Heatwave":

                (39,82,4),

            "Rainstorm":

                (22,96,18)

        }

        if preset in presets:

            t,h,w = presets[preset]

            self.temperature = t
            self.humidity = h
            self.wind_speed = w

    def emergency_mode(
        self,
        enabled=True
    ):

        self.emergency = enabled

        if enabled:

            self.temperature += 4

            self.humidity += 8

    def inject_event(
        self,
        event_name
    ):

        if event_name == "Heat Wave":

            self.temperature += 8

        elif event_name == "Heavy Rain":

            self.humidity = 95

        elif event_name == "Thunderstorm":

            self.weather_code = 95

        elif event_name == "Cold Front":

            self.temperature -= 10

        elif event_name == "Strong Wind":

            self.wind_speed = 35

        elif event_name == "Sensor Failure":

            self.last_reading = None

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):
        """
        Restores default conditions.
        """

        self._history.clear()

        self.last_reading = None

        self.total_readings = 0

        self.maximum_temperature = float("-inf")
        self.minimum_temperature = float("inf")

        self.maximum_humidity = float("-inf")
        self.minimum_humidity = float("inf")

        self.maximum_heat_index = float("-inf")
        self.minimum_heat_index = float("inf")

        self.total_temperature = 0

        self.total_humidity = 0

        self.total_heat_index = 0

        self.wind_speed = 8

        self.pressure = 1013

        self.uv_index = 0

        self.weather_code = 0

        self.weather_description = "Clear Sky"


# ============================================================
# Singleton
# ============================================================

heat_simulator = HeatSimulator()