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

        self.frames_processed = 0

        self.total_people_detected = 0

        self.total_alerts = 0

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

    # ========================================================
    # Summary
    # ========================================================

    def summary(self) -> Dict:
        """
        Returns all metrics.
        """

        return {
            "uptime_seconds": self.uptime(),
            "frames_processed": self.frames_processed,
            "average_fps": self.average_fps(),
            "average_processing_time": self.average_processing_time(),
            "total_people_detected": self.total_people_detected,
            "total_alerts": self.total_alerts
        }

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