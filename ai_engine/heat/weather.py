"""
============================================================
Astravon Live Arena
Weather Service

Purpose:
    Retrieves live weather information for the
    camera location using Open-Meteo.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import time
import requests

from utils.logger import get_logger


logger = get_logger("Weather")


class WeatherService:
    """
    Downloads live weather for the camera location.

    Data is cached to avoid excessive API requests.
    """

    def __init__(
        self,
        camera,
        refresh_interval: int = 300
    ):

        self.camera = camera

        self.refresh_interval = refresh_interval

        self.last_update = 0

        self.cache = None

    # ==========================================================
    # Fetch
    # ==========================================================

    def fetch(self):

        now = time.time()
        latitude = self.camera.latitude
        longitude = self.camera.longitude

        if (
            self.cache is not None and
            now - self.last_update <
            self.refresh_interval
        ):
            return self.cache

        url = (

            "https://api.open-meteo.com/v1/forecast"

            f"?latitude={latitude}"

            f"&longitude={longitude}"

            "&current="

            "temperature_2m,"

            "relative_humidity_2m,"

            "apparent_temperature,"

            "wind_speed_10m,"

            "weather_code"

        )

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            current = response.json()["current"]

            self.cache = {

                "temperature":
                    current["temperature_2m"],

                "humidity":
                    current["relative_humidity_2m"],

                "heat_index":
                    current["apparent_temperature"],

                "wind_speed":
                    current["wind_speed_10m"],

                "weather_code":
                    current["weather_code"],

                "timestamp":
                    current["time"]

            }

            self.last_update = now

            logger.info(
                "Weather updated."
            )

            return self.cache

        except Exception as error:

            logger.error(error)

            if self.cache:

                return self.cache

            return {

                "temperature": 25.0,
                "humidity": 50.0,
                "heat_index": 25.0,
                "wind_speed": 0.0,
                "weather_code": -1,
                "timestamp": None

            }

    # ==========================================================
    # Temperature
    # ==========================================================

    def temperature(self):

        return self.fetch()["temperature"]

    # ==========================================================
    # Humidity
    # ==========================================================

    def humidity(self):

        return self.fetch()["humidity"]

    # ==========================================================
    # Heat Index
    # ==========================================================

    def heat_index(self):

        return self.fetch()["heat_index"]

    # ==========================================================
    # Wind Speed
    # ==========================================================

    def wind_speed(self):

        return self.fetch()["wind_speed"]

    # ==========================================================
    # Complete Weather
    # ==========================================================

    def reading(self):

        return self.fetch()