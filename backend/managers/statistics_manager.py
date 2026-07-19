"""
============================================================
Astravon Live Arena
Statistics Manager

Purpose:
    Centralized statistics aggregation for all cameras.

Responsibilities:
    • Store latest statistics per camera
    • Maintain history
    • Aggregate system statistics
    • Compute averages
    • Provide dashboard summaries
    • Thread-safe

Author:
    House of Astravon

Version:
    2.0.0
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
from threading import Lock
from typing import Dict, Optional, List

from utils.logger import get_logger

logger = get_logger("StatisticsManager")


# ============================================================
# Camera Statistics
# ============================================================

@dataclass
class CameraStatistics:

    camera_id: str

    timestamp: datetime = field(default_factory=datetime.utcnow)

    people: int = 0

    occupancy: float = 0.0

    density: float = 0.0

    risk_score: float = 0.0

    risk_level: str = "Low"

    temperature: float = 0.0

    humidity: float = 0.0

    fps: float = 0.0

    inference_ms: float = 0.0

    history: deque = field(
        default_factory=lambda: deque(maxlen=300)
    )


# ============================================================
# Statistics Manager
# ============================================================

class StatisticsManager:

    def __init__(self):

        self._statistics: Dict[str, CameraStatistics] = {}

        self._lock = Lock()

        logger.info("Statistics Manager initialized.")

    # --------------------------------------------------------
    # Camera Registration
    # --------------------------------------------------------

    def register_camera(
        self,
        camera_id: str
    ):

        with self._lock:

            if camera_id not in self._statistics:

                self._statistics[camera_id] = CameraStatistics(
                    camera_id=camera_id
                )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    def update(
        self,
        camera_id: str,
        statistics: dict
    ):

        if camera_id not in self._statistics:

            self.register_camera(camera_id)

        stat = self._statistics[camera_id]

        with self._lock:

            stat.timestamp = datetime.utcnow()

            detection = statistics.get(
                "detection",
                {}
            )

            stat.people = detection.get(
                "people_count",
                stat.people
            )

            stat.occupancy = statistics.get(
                "occupancy",
                {}
            ).get(
                "occupancy_percentage",
                stat.occupancy
            )

            density = statistics.get(
                "density",
                {}
            )

            stat.density = density.get(
                "average_density",
                stat.density
            )

            risk = statistics.get("risk", {})

            stat.risk_score = risk.get(
                "risk_score",
                stat.risk_score
            )

            stat.risk_level = risk.get(
                "risk_level",
                stat.risk_level
            )

            weather = statistics.get("weather", {})

            stat.temperature = weather.get(
                "temperature",
                stat.temperature
            )

            stat.humidity = weather.get(
                "humidity",
                stat.humidity
            )

            performance = statistics.get(
                "performance",
                {}
            )

            stat.fps = performance.get(
                "current_fps",
                stat.fps
            )

            detector = performance.get(
                "detector",
                {}
            )

            stat.inference_ms = detector.get(
                "processing_time_ms",
                stat.inference_ms
            )

            stat.history.append({

                "timestamp": stat.timestamp.isoformat(),

                "people": stat.people,

                "risk": stat.risk_score,

                "occupancy": stat.occupancy,

                "density": stat.density

            })

    # --------------------------------------------------------
    # Add Statistics (AI Service)
    # --------------------------------------------------------

    def add_statistics(
        self,
        statistics: dict
    ):
        """
        Accepts a complete statistics object from the AI Service
        and routes it to the appropriate camera.
        """

        camera = statistics.get("camera", {})

        camera_id = camera.get(
            "camera_id",
            "default"
        )

        self.update(
            camera_id=camera_id,
            statistics=statistics
        )

    # --------------------------------------------------------
    # Latest
    # --------------------------------------------------------

    def latest(
        self,
        camera_id: str
    ) -> Optional[dict]:

        stat = self._statistics.get(camera_id)

        if stat is None:

            return None

        return {

            "camera_id": stat.camera_id,

            "timestamp": stat.timestamp.isoformat(),

            "people": stat.people,

            "occupancy": stat.occupancy,

            "density": stat.density,

            "risk_score": stat.risk_score,

            "risk_level": stat.risk_level,

            "temperature": stat.temperature,

            "humidity": stat.humidity,

            "fps": stat.fps,

            "inference_ms": stat.inference_ms

        }

    # --------------------------------------------------------
    # History
    # --------------------------------------------------------

    def history(
        self,
        camera_id: str
    ) -> List[dict]:

        stat = self._statistics.get(camera_id)

        if stat is None:

            return []

        return list(stat.history)

    # --------------------------------------------------------
    # Dashboard Summary
    # --------------------------------------------------------

    def dashboard(self):

        if not self._statistics:

            return {}

        cameras = len(self._statistics)

        total_people = sum(
            s.people
            for s in self._statistics.values()
        )

        average_risk = round(

            sum(
                s.risk_score
                for s in self._statistics.values()
            ) / cameras,

            2

        )

        average_fps = round(

            sum(
                s.fps
                for s in self._statistics.values()
            ) / cameras,

            2

        )

        average_inference = round(

            sum(
                s.inference_ms
                for s in self._statistics.values()
            ) / cameras,

            2

        )

        return {

            "camera_count": cameras,

            "total_people": total_people,

            "average_risk": average_risk,

            "average_fps": average_fps,

            "average_inference_ms": average_inference

        }

    # --------------------------------------------------------
    # Snapshot
    # --------------------------------------------------------

    def snapshot(self):

        return {

            cid: self.latest(cid)

            for cid in self._statistics

        }
    
    # --------------------------------------------------------
    # System Snapshot
    # --------------------------------------------------------

    def full_snapshot(self):

        return {

            "generated_at": datetime.utcnow().isoformat(),

            "camera_count": self.camera_count,

            "dashboard": self.dashboard(),

            "cameras": self.snapshot()

        }

    # --------------------------------------------------------
    # Remove Camera
    # --------------------------------------------------------

    def remove(
        self,
        camera_id: str
    ):

        with self._lock:

            self._statistics.pop(camera_id, None)

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(self):

        with self._lock:

            self._statistics.clear()

            logger.info(
                "Statistics Manager reset."
            )

    # --------------------------------------------------------
    # Properties
    # --------------------------------------------------------

    @property
    def camera_count(self):

        return len(self._statistics)