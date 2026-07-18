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
from collections import deque
from datetime import datetime

from utils.logger import get_logger


logger = get_logger("Weather")

WEATHER_CODES = {

    0: "Clear Sky",

    1: "Mainly Clear",

    2: "Partly Cloudy",

    3: "Overcast",

    45: "Fog",

    48: "Depositing Rime Fog",

    51: "Light Drizzle",

    53: "Moderate Drizzle",

    55: "Dense Drizzle",

    61: "Light Rain",

    63: "Moderate Rain",

    65: "Heavy Rain",

    71: "Snow",

    80: "Rain Showers",

    95: "Thunderstorm"
}


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

        self.successful_requests = 0
        self.failed_requests = 0

        self.history = deque(maxlen=500)

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

                "weather_desc": WEATHER_CODES.get(
                    current["weather_code"],
                    "Unknown"
                ),

                "api_health": {

                    "successful": self.successful_requests,

                    "failed": self.failed_requests

                },

                "timestamp":
                    current["time"]

            }

            self.last_update = now
            self.successful_requests += 1

            logger.info(
                "Weather updated."
            )

            self.history.append(self.cache)

            return self.cache

        except Exception as error:

            logger.error(error)
            self.failed_requests += 1

            if self.cache:

                return self.cache

            return {
                "temperature": 25.0,
                "humidity": 50.0,
                "heat_index": 25.0,
                "wind_speed": 0.0,
                "weather_code": -1,
                "weather_desc": "Unknown",
                "api_health": {
                    "successful": self.successful_requests,
                    "failed": self.failed_requests
                },
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
    
    def history(self):

     return list(self.history)
    
    def averages(self):

        if not self.history:
            return {}

        return {

            "temperature":

                round(

                    sum(x["temperature"] for x in self.history)

                    /

                    len(self.history),

                    2

                ),

            "humidity":

                round(

                    sum(x["humidity"] for x in self.history)

                    /

                    len(self.history),

                    2

                )
        }

    # ==========================================================
    # Wind Speed
    # ==========================================================

    def wind_speed(self):

        return self.fetch()["wind_speed"]
    
    def trend(self):

        if len(self.history) < 2:
            return "Stable"

        last = self.history[-1]["temperature"]

        prev = self.history[-2]["temperature"]

        if last > prev:
            return "Rising"

        elif last < prev:
            return "Falling"

        return "Stable"
    
    def severity(self):

        weather = self.fetch()

        temp = weather["temperature"]

        wind = weather["wind_speed"]

        if temp >= 40:
            return "Extreme"

        if temp >= 35:
            return "High"

        if wind >= 40:
            return "High"

        return "Normal"
    
    def heat_stress(self):

        hi = self.fetch()["heat_index"]

        if hi < 27:
            return "Safe"

        elif hi < 32:
            return "Caution"

        elif hi < 41:
            return "Extreme Caution"

        elif hi < 54:
            return "Danger"

        return "Extreme Danger"
    
    def wind_level(self):

        speed = self.fetch()["wind_speed"]

        if speed < 5:
            return "Calm"

        elif speed < 15:
            return "Light"

        elif speed < 30:
            return "Moderate"

        return "Strong"
    
    def comfort(self):

        weather = self.fetch()

        temp = weather["temperature"]

        humidity = weather["humidity"]

        if 18 <= temp <= 27 and humidity < 70:
            return "Comfortable"

        if temp > 35:
            return "Very Hot"

        if humidity > 85:
            return "Humid"

        return "Normal"
    
    def summary(self):

        weather = self.fetch()

        return {

            "temperature": weather["temperature"],

            "humidity": weather["humidity"],

            "heat_index": weather["heat_index"],

            "wind_speed": weather["wind_speed"],

            "weather_code": weather["weather_code"],

            "weather_desc": weather["weather_desc"],

            "severity": self.severity(),

            "heat_stress": self.heat_stress(),

            "comfort": self.comfort(),

            "trend": self.trend(),

            "timestamp": datetime.utcnow().isoformat()
        }

    # ==========================================================
    # Module Information
    # ==========================================================

    def info(self) -> dict:
        """
        Returns Weather Service status.
        """

        return {

            "module": "Weather Service",

            "status": "Running",

            "provider": "Open-Meteo",

            "camera": self.camera.name,

            "refresh_interval": self.refresh_interval,

            "last_update": self.last_update,

            "cached": self.cache is not None,

            "location": {

                "latitude": self.camera.latitude,

                "longitude": self.camera.longitude,

                "city": self.camera.city,

                "country": self.camera.country

            }

        }

    # ==========================================================
    # Complete Weather
    # ==========================================================

    def reading(self):

        return self.fetch()