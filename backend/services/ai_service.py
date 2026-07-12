"""
============================================================
Astravon Live Arena
AI Service

Purpose:
    Business logic for AI operations.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime

from backend.schemas.detection import DetectionRequest
from backend.schemas.alert import AlertCreateRequest
from backend.schemas.statistics import StatisticsRequest

from backend.utils.logger import get_logger

from backend.utils.constants import (
    DENSITY_LOW,
    DEFAULT_TEMPERATURE,
    DEFAULT_HUMIDITY,
    DEFAULT_HEAT_INDEX,
    RISK_LOW
)

from backend.utils.validators import (
    validate_confidence,
    validate_risk_score
)

from backend.utils.helpers import (
    calculate_risk_level,
    calculate_density,
    calculate_heat_index
)


class AIService:
    """
    Handles AI-related operations.

    Future responsibilities:
    - Communicate with AI Engine
    - Store statistics
    - Trigger alerts
    - Broadcast WebSocket updates
    """
    logger = get_logger(
        "AIService"
    )

    def __init__(self):

        self.current_statistics = {
            "people_count": 0,
            "density": DENSITY_LOW,
            "occupancy": 0,
            "temperature": DEFAULT_TEMPERATURE,
            "humidity": DEFAULT_HUMIDITY,
            "heat_index": DEFAULT_HEAT_INDEX,
            "risk_score": 0,
            "risk_level": RISK_LOW,
            "timestamp": datetime.now().isoformat()
        }

        self.statistics_history = []

        self.alerts = []

    # ========================================================
    # Detection
    # ========================================================

    def process_detection(
        self,
        request: DetectionRequest
    ) -> dict:
        """
        Processes AI detection data.
        """
        if not validate_risk_score(
            request.risk_score
        ):

            self.logger.warning(
                "Invalid risk score detected"
            )

            raise ValueError(
                "Invalid risk score"
            )
        
        self.logger.info(
            "Processing AI detection data"
        )

        self.current_statistics = {
            "people_count": request.people_count,
            "density": request.density,
            "occupancy": request.occupancy,
            "temperature": request.temperature,
            "humidity": request.humidity,
            "heat_index": request.heat_index,
            "risk_score": request.risk_score,
            "risk_level": request.risk_level,
            "timestamp": datetime.now().isoformat()
        }

        self.statistics_history.append(
            self.current_statistics.copy()
        )

        self.logger.info(
            "AI detection completed"
        )

        return self.current_statistics

    # ========================================================
    # Statistics
    # ========================================================

    def get_statistics(self):

        return self.current_statistics

    def save_statistics(
        self,
        request: StatisticsRequest
    ):

        return self.process_detection(request)

    def get_statistics_history(self):

        return self.statistics_history

    def delete_statistics(
        self,
        statistics_id: int
    ) -> bool:

        if statistics_id < len(self.statistics_history):

            del self.statistics_history[statistics_id]

            return True

        return False

    # ========================================================
    # Dashboard Values
    # ========================================================

    def get_density(self):

        return {
            "density": self.current_statistics["density"]
        }

    def get_temperature(self):

        return {
            "temperature": self.current_statistics["temperature"]
        }

    def get_occupancy(self):

        return {
            "occupancy": self.current_statistics["occupancy"]
        }

    def get_current_risk(self):

        return {
            "risk_score": self.current_statistics["risk_score"],
            "risk_level": self.current_statistics["risk_level"]
        }

    def get_highest_crowd(self):

        if not self.statistics_history:

            return {
                "people_count": 0
            }

        highest = max(
            self.statistics_history,
            key=lambda item: item["people_count"]
        )

        return highest

    def get_statistics_summary(self):

        total_records = len(self.statistics_history)

        return {
            "records": total_records,
            "latest": self.current_statistics
        }

    # ========================================================
    # Alerts
    # ========================================================

    def get_alerts(self):

        return self.alerts

    def create_alert(
        self,
        request: AlertCreateRequest
    ):

        alert = {
            "id": len(self.alerts) + 1,
            "title": request.title,
            "severity": request.severity,
            "description": request.description,
            "resolved": False,
            "created_at": datetime.now().isoformat()
        }

        self.alerts.append(alert)

        return alert

    def get_alert(
        self,
        alert_id: int
    ):

        for alert in self.alerts:

            if alert["id"] == alert_id:

                return alert

        return None

    def resolve_alert(
        self,
        alert_id: int
    ):

        alert = self.get_alert(alert_id)

        if alert:

            alert["resolved"] = True

        return alert

    def delete_alert(
        self,
        alert_id: int
    ):

        alert = self.get_alert(alert_id)

        if alert:

            self.alerts.remove(alert)

            return True

        return False

    def get_alert_statistics(self):

        return {
            "total": len(self.alerts),
            "active": len(
                [
                    a
                    for a in self.alerts
                    if not a["resolved"]
                ]
            ),
            "resolved": len(
                [
                    a
                    for a in self.alerts
                    if a["resolved"]
                ]
            )
        }

    # ========================================================
    # Simulation
    # ========================================================

    def reset(self):
        """
        Reset demo data.
        """

        self.current_statistics = {
            "people_count": 0,
            "density": "Low",
            "occupancy": 0,
            "temperature": 25.0,
            "humidity": 50.0,
            "heat_index": 27.0,
            "risk_score": 0,
            "risk_level": "Low",
            "timestamp": datetime.now().isoformat()
        }

        self.statistics_history.clear()

        self.alerts.clear()

        return True