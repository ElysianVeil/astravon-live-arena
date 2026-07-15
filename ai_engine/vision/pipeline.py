"""
============================================================
Astravon Live Arena
Vision Pipeline

Purpose:
    Connects the camera, preprocessing,
    YOLO detection, ByteTrack tracking,
    and visualization into a single pipeline.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Dict, List, Optional

import cv2
import supervision as sv
import time
from datetime import datetime

from config import settings
from constants import PERSON_CLASS_ID

from utils.logger import get_logger
from api.detection import (DetectionRequest, DetectedObject)

from vision.camera import Camera
from vision.stream import VideoStream
from vision.preprocessing import ImagePreprocessor
from vision.detector import YOLODetector
from vision.tracker import PersonTracker
from vision.drawing import Drawing

from crowd.counter import CrowdCounter
from crowd.density import CrowdDensity
from crowd.occupancy import OccupancyAnalyzer

from heat.temperature import TemperatureManager
from heat.humidity import HumidityManager
from heat.heat_index import HeatIndexCalculator

from risk.analyzer import RiskAnalyzer

from analytics.metrics import MetricsManager

from api.output import OutputManager


# ============================================================
# Vision Pipeline
# ============================================================

logger = get_logger("Pipeline")

class VisionPipeline:
    """
    Main AI processing pipeline.

    Camera
        ↓
    Stream
        ↓
    YOLO
        ↓
    ByteTrack
        ↓
    Output
    """

    def __init__(
        self,
        camera_source=0,
        confidence: float = 0.5
    ):

        self.preprocessor = ImagePreprocessor()

        self.counter = CrowdCounter()

        self.density = CrowdDensity()

        self.occupancy = OccupancyAnalyzer()

        self.temperature = TemperatureManager()

        self.humidity = HumidityManager()

        self.heat_index = HeatIndexCalculator()

        self.risk = RiskAnalyzer()

        self.metrics = MetricsManager()

        self.output = OutputManager()

        self.camera = Camera(camera_source)

        self.stream = VideoStream(self.camera)

        self.detector = YOLODetector(
            confidence=confidence
        )

        self.tracker = PersonTracker()

    # ========================================================
    # Start
    # ========================================================

    def start(self):
        """
        Starts the video stream.
        """

        self.stream.start()

        logger.info("Waiting for first camera frame...")

        timeout = 5
        start = time.time()

        while not self.stream.has_frame():

            if time.time() - start > timeout:
                raise RuntimeError("Camera produced no frames.")

            time.sleep(0.05)

        logger.info("First frame received.")

    # ========================================================
    # Stop
    # ========================================================

    def stop(self):
        """
        Stops the pipeline.
        """
        self.output.shutdown()
        
        self.stream.close()

    # ========================================================
    # Process One Frame
    # ========================================================

    def process(self) -> Optional[Dict]:
        """
        Processes one frame.

        Returns:
            Dictionary containing:

            frame
            tracked_people
            detections
            people_count
        """
        start_time = time.perf_counter()

        frame = self.stream.get_frame()

        if frame is None:
            logger.warning(
                "Waiting for the first frame..."
            )

            return None
        
        frame = self.preprocessor.process(frame)
        detection_result = self.detector.detect(frame)

        # for d in detection_result.detections:
        #     print(d)
        #     for k, v in d.items():
        #         print(k, type(v), v)

        objects = []

        for detection in detection_result.detections:

            x1, y1, x2, y2 = detection["bbox"]

            objects.append(
                DetectedObject(
                    label=detection["class_name"],
                    confidence=float(detection["confidence"]),
                    x=int(x1),
                    y=int(y1),
                    width=int(x2 - x1),
                    height=int(y2 - y1),
                )
            )
        # ---------------------------------------
        # ByteTrack
        # ---------------------------------------

        tracked = self.tracker.update(
            detection_result.supervision
        )
        # print(f"Tracked: {tracked}")

        tracks = self.tracker.get_tracks(
            tracked
        )
        # print(f"Tracks: {tracks}")
        print(f"Track count: {len(tracks)}")
        people_count = self.counter.count_people(tracks)

        density_data = self.density.analyze(people_count)

        density = density_data["density_level"]

        occupancy_data = self.occupancy.analyze(people_count)

        occupancy = occupancy_data["occupancy_percentage"]

        reading = self.temperature.reading()

        temperature = reading["temperature"]

        reading_2 = self.humidity.reading()

        humidity = reading_2["humidity"]

        heat_index = self.heat_index.calculate(
            temperature,
            humidity
        )

        risk = self.risk.analyze(

            people_count=people_count,
            venue_capacity=self.density.get_capacity(),
            density=density,
            occupancy=occupancy,
            temperature=temperature,
            humidity=humidity

        )

        if risk["risk_level"] in ["High", "Critical"]:
            self.output.send_alert(risk)

        logger.info(
            f"People detected: {people_count}"
        )

        # ---------------------------------------
        # Draw boxes
        # ---------------------------------------

        output = frame.copy()

        output = Drawing.draw_detections(
            output,
            detection_result.detections
        )

        output = Drawing.draw_tracks(
            output,
            tracks
        )

        output = Drawing.draw_statistics(

            output,

            people_count,

            density,

            occupancy,

            temperature,

            risk["risk_score"]

        )

        height, width = output.shape[:2]

        camera_payload = {
            "frame": output,
            "width": width,
            "height": height,
            "fps": float(self.metrics.average_fps())
        }

        self.output.send_camera_frame(camera_payload)

        processing_time = time.perf_counter() - start_time

        self.metrics.record_frame(
            processing_time=processing_time,
            people_detected=people_count
        )

        # Record an alert if the risk is elevated
        if risk["risk_score"] >= 70:      # choose your threshold
            self.metrics.record_alert()

        payload = DetectionRequest(

            people_count=people_count,

            detected_objects=len(objects),

            density=density,

            occupancy=int(occupancy),

            temperature=float(temperature),

            humidity=float(humidity),

            heat_index=float(heat_index),

            risk_score=int(risk["risk_score"]),

            risk_level=risk["risk_level"],

            confidence=(
                max(obj.confidence for obj in objects)
                if objects else 0.0
            ),

            fps=float(self.metrics.average_fps()),

            processing_time=float(
                self.metrics.average_processing_time()
            ),

            timestamp=datetime.utcnow(),

            objects=objects
        )

        self.output.send_detection(payload.model_dump(mode="json"))

        # ---------------------------------------
        # Statistics
        # ---------------------------------------
        statistics = {
            "people_count": people_count,
            "occupancy": occupancy,
            "density": density,
            "temperature": temperature,
            "humidity": humidity,
            "heat_index": heat_index,
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
            "detected_objects": len(detection_result.detections),
            "confidence": (
                max(obj.confidence for obj in objects)
                if objects else 0.0
            ),
            "processing_time": processing_time,
            "fps": float(self.metrics.average_fps())
        }

        self.output.send_statistics(statistics)

        # people_count = len(tracks)

        result = {
            "frame": output,
            "tracks": tracks,
            "detections": detection_result.detections,
            "people_count": people_count,
            "density": density,
            "occupancy": occupancy,
            "temperature": temperature,
            "heat_index": heat_index,
            "risk": risk
        }

        return result

    # ========================================================
    # Run Forever
    # ========================================================

    def run(self):
        """
        Starts a live AI session.
        """
        logger.info("Starting AI Engine...")

        self.start()

        try:

            while True:

                result = self.process()

                if result is None:
                    continue

                cv2.imshow(
                    "Astravon Live Arena",
                    result["frame"]
                )

                key = cv2.waitKey(1)

                if key == ord("q"):
                    break

        finally:

            self.stop()

            cv2.destroyAllWindows()