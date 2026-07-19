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

# from backend.utils.constants import (
#     DENSITY_LOW,
#     DEFAULT_TEMPERATURE,
#     DEFAULT_HUMIDITY,
#     DEFAULT_HEAT_INDEX,
#     RISK_LOW
# )

from backend.utils.validators import (
    validate_confidence,
    validate_risk_score
)

# from backend.utils.helpers import (
#     calculate_risk_level,
#     calculate_density,
#     calculate_heat_index
# )


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

    def __init__(
        self,
        statistics_manager=None,
        alert_manager=None,
        camera_manager=None,
        notification_service=None,
        archive_storage=None
    ):

        self.statistics_manager = statistics_manager
        self.alert_manager = alert_manager
        self.camera_manager = camera_manager
        self.notification_service = notification_service
        self.archive_storage = archive_storage
       # ========================================================
        # Runtime State
        # ========================================================

        self.current_detection = {}

        self.current_statistics = {}

        self.current_alerts = []

        self.active_cameras = {}

        # Historical snapshots
        self.statistics_history = []

        # Current risk cache
        self.current_risk = {
            "risk_score": 0,
            "risk_level": "Low"
        }

        self.engine_status = {
            "status": "Running",
            "started_at": datetime.utcnow().isoformat(),
            "processed_frames": 0,
            "statistics_generated": 0,
            "detections_processed": 0
        }
        


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
        if not validate_confidence(request.confidence):
            raise ValueError("Invalid confidence")

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

        self.current_detection = {
            "camera_id": request.camera_id,
            "camera_name": request.camera_name,

            "venue": request.venue,

            "city": request.city,
            "country": request.country,

            "latitude": request.latitude,
            "longitude": request.longitude,

            "people_count": request.people_count,
            "occupancy": request.occupancy,
            "density": request.density,

            "temperature": request.temperature,
            "humidity": request.humidity,
            "heat_index": request.heat_index,

            "wind_speed": request.wind_speed,
            "weather_code": request.weather_code,
            "weather_desc": request.weather_desc,

            "risk_score": request.risk_score,
            "risk_level": request.risk_level,

            "detected_objects": request.detected_objects,

            "confidence": request.confidence,
            "processing_time": request.processing_time,
            "fps": request.fps,

            "timestamp": datetime.now().isoformat()
        }
        self.engine_status["processed_frames"] += 1

        self.engine_status["detections_processed"] += 1

        camera = self.active_cameras.setdefault(

            request.camera_id,

            {}

        )

        camera.update({

            "camera_name": request.camera_name,

            "last_detection": datetime.utcnow().isoformat(),

            "people": request.people_count,

            "fps": request.fps,

            "risk": request.risk_score,

            "connected": True

        })

        if self.statistics_manager:

            self.statistics_manager.add_statistics(
                self.current_detection.copy()
            )

        if self.archive_storage:

            self.archive_storage.archive_detection(
                self.current_detection
            )
            

        if self.notification_service:

            self.notification_service.broadcast_detection(

                self.current_detection

            )

        self.evaluate_detection_alerts()

        self.logger.info(

            f"[{request.camera_name}] "

            f"People={request.people_count} "

            f"Risk={request.risk_score} "

            f"FPS={request.fps}"

        )

        self.logger.info(
            "AI detection completed"
        )

        return self.current_detection
    
    # ========================================================
    # Process Statistics
    # ========================================================

    def process_statistics(
        self,
        request: StatisticsRequest
    ) -> dict:
        """
        Processes AI detection data.
        """
        if not validate_risk_score(
            request.risk["risk_score"]
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

        self.current_statistics = request.model_dump()

        self.statistics_history.append(
            self.current_statistics.copy()
        )

        self.current_risk = self.current_statistics.get(
            "risk",
            {}
        )

        self.engine_status["statistics_generated"] += 1

        self.engine_status["last_statistics"] = datetime.utcnow().isoformat()

        if self.camera_manager:

            self.camera_manager.update_statistics(

                camera_id = self.current_detection.get(
                    "camera_id",
                    "unknown"
                ),

                statistics=self.current_statistics
            )

            self.statistics_manager.add_statistics(
                self.current_statistics.copy()
            )
        
        if self.notification_service:

            self.notification_service.statistics_update(

                self.current_statistics

            )

        if self.archive_storage:

            self.archive_storage.archive_statistics(

                self.current_statistics

            )

        self.evaluate_statistics_alerts()

        self.logger.info(
            "AI detection completed"
        )

        return self.current_statistics


    # ========================================================
    # Automatic Detection Alerts
    # ========================================================

    def evaluate_detection_alerts(self):

        if not self.alert_manager:

            return

        risk = self.current_detection.get(
            "risk_score",
            0
        )

        people = self.current_detection.get(
            "people_count",
            0
        )

        if risk >= 80:

            self.alert_manager.create(

                title="Critical Crowd Risk",

                severity="Critical",

                description="AI detected extremely dangerous conditions."

            )

        elif people >= 200:

            self.alert_manager.create(

                title="High Occupancy",

                severity="Warning",

                description="Crowd approaching capacity."

            )

    # ========================================================
    # Automatic Statistics Alerts
    # ========================================================

    def evaluate_statistics_alerts(self):

        if not self.alert_manager:

            return

        risk = (
            self.current_statistics
            .get("risk", {})
            .get("risk_score", 0)
        )

        congestion = (
            self.current_statistics
            .get("congestion", {})
            .get("current_score", 0)
        )

        occupancy = (
            self.current_statistics
            .get("occupancy", {})
            .get("occupancy_percentage", 0)
        )
        if risk >= 80:

            self.alert_manager.create(

                title="Critical Risk",

                severity="Critical",

                description="Overall venue risk is critical."

            )

        elif congestion >= 70:

            self.alert_manager.create(

                title="Heavy Congestion",

                severity="Warning",

                description="Crowd congestion becoming dangerous."

            )

        elif occupancy >= 95:

            self.alert_manager.create(

                title="Venue Full",

                severity="Critical",

                description="Venue is almost at capacity."

            )

    def get_engine_status(self):

        return self.engine_status

    def get_active_cameras(self):

        return self.active_cameras


    def get_camera_status(
        self,
        camera_id: str
    ):

        return self.active_cameras.get(camera_id)

    # ========================================================
    # Statistics
    # ========================================================

    def get_statistics(self):

        return self.current_statistics

    def save_statistics(
        self,
        request: StatisticsRequest
    ):

        return self.process_statistics(request)

    # def get_statistics_history(self):

    #     return self.statistics_history

    # def delete_statistics(
    #     self,
    #     statistics_id: int
    # ) -> bool:

    #     if statistics_id < len(self.statistics_history):

    #         del self.statistics_history[statistics_id]

    #         return True

    #     return False

    # ========================================================
    # Dashboard Values
    # ========================================================

    def get_engine(self):

        return self.current_statistics.get(
            "engine",
            {}
        )


    def get_camera(self):

        return self.current_statistics.get(
            "camera",
            {}
        )


    def get_detection(self):

        return self.current_statistics.get(
            "detection",
            {}
        )


    def get_weather(self):

        return self.current_statistics.get(
            "weather",
            {}
        )


    def get_density(self):

        return self.current_statistics.get(
            "density",
            {}
        )


    def get_occupancy(self):

        return self.current_statistics.get(
            "occupancy",
            {}
        )


    def get_congestion(self):

        return self.current_statistics.get(
            "congestion",
            {}
        )


    def get_risk(self):

        return self.current_statistics.get(
            "risk",
            {}
        )


    def get_trends(self):

        return self.current_statistics.get(
            "trends",
            {}
        )


    def get_performance(self):

        return self.current_statistics.get(
            "performance",
            {}
        )
    
    # ============================================================
    # Delete Statistics
    # ============================================================

    def delete_statistics(
        self,
        statistics_id: int
    ) -> bool:

        if (
            statistics_id < 1
            or
            statistics_id > len(self.statistics_history)
        ):
            return False

        del self.statistics_history[
            statistics_id - 1
        ]

        return True
    
    # ============================================================
    # Current Temperature
    # ============================================================

    def get_temperature(self):

        return {
            "temperature":
                self.current_detection.get(
                    "temperature",
                    0
                ),
            "unit": "°C"
        }
    
    # ============================================================
    # Statistics History
    # ============================================================

    def get_statistics_history(self):
        """
        Returns historical statistics.
        """

        return self.statistics_history 
       
    # ============================================================
    # Statistics Summary
    # ============================================================

    def get_statistics_summary(self):

        history = self.statistics_history

        if not history:

            return {

                "records": 0,

                "average_people": 0,

                "highest_people": 0,

                "average_temperature": 0,

                "highest_risk": 0

            }

        people = [

            s["detection"]["people_count"]

            for s in history

        ]

        temperatures = [

            s["weather"]["temperature"]

            for s in history

        ]

        risks = [

            s["risk"]["risk_score"]

            for s in history

        ]

        return {

            "records": len(history),

            "average_people":

                sum(people)/len(people),

            "highest_people":

                max(people),

            "average_temperature":

                sum(temperatures)/len(temperatures),

            "highest_risk":

                max(risks)

        }
    
    # ============================================================
    # Highest Crowd
    # ============================================================

    def get_highest_crowd(self):
        """
        Returns the highest crowd count.
        """

        history = self.statistics_history

        if not history:

            return {

                "people_count":0,

                "timestamp":None

            }

        highest = max(

            history,

            key=lambda x:

                x["detection"]["people_count"]

        )

        return {

            "people_count":

                highest["detection"]["people_count"],

            "timestamp":

                highest["timestamp"]

        }
    
    # ============================================================
    # Current Risk
    # ============================================================

    def get_current_risk(self):
        """
        Returns current crowd risk.
        """

        return self.current_risk
    


    # ========================================================
    # Simulation
    # ========================================================

    def reset(self):
        """
        Reset demo data.
        """

        self.current_detection={}

        self.current_statistics={}

        self.current_alerts=[]

        self.active_cameras.clear()

        self.engine_status={

            "status":"Running",

            "started_at":datetime.utcnow().isoformat(),

            "processed_frames":0,

            "statistics_generated":0,

            "detections_processed":0

        }

        return True