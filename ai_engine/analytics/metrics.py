"""
============================================================
Astravon Live Arena
AI Metrics

Purpose:
    Computes performance metrics for the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import time
from collections import deque
from statistics import mean
from typing import Dict, Deque


# ============================================================
# Metrics Manager
# ============================================================

class MetricsManager:
    """
    Tracks AI Engine performance metrics.
    """

    def __init__(self) -> None:

        self.start_time = time.time()

        self.engine_started = True

        self.engine_status = "Running"

        self.last_frame_timestamp = None

        self.last_alert_timestamp = None

        self.frames_processed = 0

        self.maximum_fps = 0.0

        self.minimum_fps = float("inf")

        self.total_people_detected = 0

        self.maximum_people_detected = 0

        self.frames_with_people = 0

        self.empty_frames = 0

        self.current_fps = 0.0

        self.current_processing_time = 0.0

        self.total_alerts = 0

        self.maximum_processing_time = 0.0

        self.minimum_processing_time = float("inf")

        self.processing_times: Deque[float] = deque(maxlen=500)

        self.fps_history: Deque[float] = deque(maxlen=500)

    # ========================================================
    # Frame Metrics
    # ========================================================

    def record_frame(
        self,
        processing_time: float,
        people_detected: int
    ) -> None:
        """
        Records one processed frame.
        """

        self.frames_processed += 1

        self.total_people_detected += people_detected

        self.current_processing_time = processing_time

        if processing_time > 0:
            self.current_fps = round(
                1.0 / processing_time,
                2
            )

        self.maximum_fps = max(
            self.maximum_fps,
            self.current_fps
        )

        self.minimum_fps = min(
            self.minimum_fps,
            self.current_fps
        )

        self.maximum_processing_time = max(
            self.maximum_processing_time,
            processing_time
        )

        self.minimum_processing_time = min(
            self.minimum_processing_time,
            processing_time
        )

        if people_detected > 0:

            self.frames_with_people += 1

        else:

            self.empty_frames += 1

        self.maximum_people_detected = max(

            self.maximum_people_detected,

            people_detected

        )

        self.processing_times.append(processing_time)

        if processing_time > 0:
            self.fps_history.append(
                1.0 / processing_time
            )

    # ========================================================
    # Alerts
    # ========================================================

    def record_alert(self) -> None:
        """
        Records an alert.
        """

        self.total_alerts += 1

        self.last_alert_timestamp = time.time()

    def throughput(self):

        uptime = self.uptime()

        if uptime <= 0:
            return 0.0

        return round(

            self.frames_processed

            /

            uptime,

            2

        )
    
    def engine_health(self):

        fps = self.average_fps()

        if fps >= 25:
            return "Excellent"

        elif fps >= 20:
            return "Good"

        elif fps >= 10:
            return "Fair"

        return "Poor"

    # ========================================================
    # Average FPS
    # ========================================================

    def average_fps(self) -> float:

        if not self.fps_history:
            return 0.0

        return round(
            mean(self.fps_history),
            2
        )

    # ========================================================
    # Average Processing Time
    # ========================================================

    def average_processing_time(self) -> float:

        if not self.processing_times:
            return 0.0

        return round(
            mean(self.processing_times),
            4
        )

    # ========================================================
    # Uptime
    # ========================================================

    def uptime(self) -> float:
        """
        Returns uptime in seconds.
        """

        return round(
            time.time() - self.start_time,
            2
        )
    
    def detection_rate(self):

        if self.frames_processed == 0:
            return 0.0

        return round(

            self.frames_with_people

            /

            self.frames_processed

            *

            100,

            2

        )
    
    def info(self):

        return {

            "engine_status": self.engine_status,

            "uptime_seconds": self.uptime(),

            "frames_processed": self.frames_processed,

            "current_fps": self.current_fps,

            "average_fps": self.average_fps(),

            "maximum_fps": self.maximum_fps,

            "minimum_fps": (
                0
                if self.minimum_fps == float("inf")
                else round(self.minimum_fps,2)
            ),

            "current_processing_time": round(
                self.current_processing_time,
                4
            ),

            "average_processing_time": self.average_processing_time(),

            "maximum_processing_time": round(
                self.maximum_processing_time,
                4
            ),

            "minimum_processing_time": (
                0
                if self.minimum_processing_time == float("inf")
                else round(self.minimum_processing_time,4)
            ),

            "frames_with_people": self.frames_with_people,

            "empty_frames": self.empty_frames,

            "maximum_people_detected": self.maximum_people_detected,

            "total_people_detected": self.total_people_detected,

            "detection_rate": self.detection_rate(),

            "alerts": self.total_alerts,

            "last_alert_timestamp": self.last_alert_timestamp,

            "throughput": self.throughput(),

            "engine_health": self.engine_health()
        }

    # ========================================================
    # Summary
    # ========================================================

    def summary(self) -> Dict:
        """
        Returns all metrics.
        """

        return self.info()

    # ========================================================
    # Reset
    # ========================================================

    def reset(self) -> None:

        self.start_time = time.time()

        self.frames_processed = 0

        self.total_people_detected = 0

        self.total_alerts = 0

        self.processing_times.clear()

        self.fps_history.clear()

        self.current_fps = 0.0

        self.current_processing_time = 0.0

        self.maximum_fps = 0.0

        self.minimum_fps = float("inf")

        self.maximum_processing_time = 0.0

        self.minimum_processing_time = float("inf")

        self.maximum_people_detected = 0

        self.frames_with_people = 0

        self.empty_frames = 0

        self.last_frame_timestamp = None

        self.last_alert_timestamp = None

        self.engine_status = "Running"


# ============================================================
# Global Instance
# ============================================================

metrics = MetricsManager()


# ============================================================
# Demonstration
# ============================================================

if __name__ == "__main__":

    metrics.record_frame(
        processing_time=0.041,
        people_detected=23
    )

    metrics.record_frame(
        processing_time=0.039,
        people_detected=21
    )

    metrics.record_alert()

    print(metrics.summary())