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

# from vision.camera import Camera
# from vision.stream import VideoStream
from vision.preprocessing import ImagePreprocessor
# from vision.camera_manager import CameraManager
from vision.detector import YOLODetector
from vision.tracker import PersonTracker
from vision.drawing import Drawing
from crowd.movement import MovementAnalyzer
from crowd.trends import CrowdTrends
from crowd.statistics import CrowdStatistics

from crowd.counter import CrowdCounter
from crowd.density import CrowdDensity
from crowd.congestion import CongestionAnalyzer
from crowd.occupancy import OccupancyAnalyzer

# from heat.temperature import TemperatureManager
# from heat.humidity import HumidityManager
from heat.heat_index import HeatIndexCalculator
from heat.weather import WeatherService

from risk.analyzer import RiskAnalyzer

# from analytics.metrics import MetricsManager

from api.output import OutputManager


from reid.feature_extractor import feature_extractor
from reid.matcher import matcher
from reid.identity_database import identity_database



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
        metrics,
        model,
        camera_manager,
        camera_source=0,
        confidence: float = 0.5
    ):

        # self.camera = Camera(camera_source)

        # self.stream = VideoStream(self.camera)

        # =====================================================
        # Cameras
        # =====================================================

        self.camera_manager = camera_manager

        self.camera_manager.add_camera(

            camera_id="camera_1",

            source=camera_source,

            name="Main Entrance"

        )

        self.preprocessor = ImagePreprocessor()

        self.counter = CrowdCounter()

        self.density = CrowdDensity()

        self.occupancy = OccupancyAnalyzer()

        self.congestion_analyzer = CongestionAnalyzer()

        # self.temperature = TemperatureManager()

        # self.humidity = HumidityManager()

        self.weather = None

        self.heat_index = HeatIndexCalculator()

        self.risk = RiskAnalyzer()

        self.metrics = metrics

        self.output = OutputManager()

        self.movement = MovementAnalyzer()

        self.trends = CrowdTrends()

        self.statistics = {}



        self.detector = YOLODetector(
            confidence=confidence,
            model=model
        )

        self.trackers = {}

        for camera_id in self.camera_manager.cameras:

            self.trackers[camera_id] = PersonTracker()
            self.statistics[camera_id] = CrowdStatistics()

        # =====================================================
        # Person Re-Identification
        # =====================================================

        self.feature_extractor = feature_extractor

        self.matcher = matcher

        self.identity_database = identity_database

    # ========================================================
    # Start
    # ========================================================

    def start(self):
        """
        Starts the video stream.
        """

        # self.stream.start()

        self.camera_manager.connect_all()

        # Camera has already connected and detected its location
        self.camera_manager.connect_all()

        self.weather_services = {}

        for camera in self.camera_manager.connected_cameras():

            self.weather_services[camera.id] = WeatherService(camera)

        logger.info(
            f"{len(self.weather_services)} weather services initialized."
        )

        # logger.info(
        #     f"Weather service initialized for "
        #     f"{self.camera.city}, {self.camera.country}"
        # )

        logger.info("Waiting for first camera frame...")

        timeout = 5
        start = time.time()

        while True:

            frames = self.camera_manager.read_all()

            if frames:

                break

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
        
        # self.stream.close()

        self.camera_manager.disconnect_all()

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

        # frame = self.stream.get_frame()

        frames = self.camera_manager.read_all()

        if not frames:
            logger.warning(
                "Waiting for the first frame..."
            )

            return None

        # if frame is None:
            

        #     return None
        
        # frame = self.preprocessor.process(frame)
        frames = self.camera_manager.read_all()

        if not frames:
            return {}

        results = {}
        for camera_id, camera_data in frames.items():

            frame = camera_data["frame"]

            camera = camera_data["camera"]

            weather = self.weather_services[camera.id]


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
        tracker = self.trackers[camera_id]

        tracked = tracker.update(
            detection_result.supervision
        )
        # print(f"Tracked: {tracked}")

        tracks = tracker.get_tracks(
            tracked
        )

        print(tracked)
        print(tracks)

        # =====================================================
        # Multi-Camera ReID
        # =====================================================

        global_tracks = []

        for track in tracks:

            x1, y1, x2, y2 = track["bbox"]

            crop = frame[y1:y2, x1:x2]

            embedding = self.feature_extractor.extract(crop)

            if embedding is None:
                continue

            global_id = self.matcher.match(
                embedding=embedding,
                camera_name=camera.name,
                camera_id=camera.id
            )

            self.identity_database.update(
                global_id=global_id,
                embedding=embedding,
                camera_id=camera.id,
                bbox=track["bbox"]
            )

            track["global_id"] = global_id

            track["embedding"] = embedding

            global_tracks.append(track)

        movement_stats = self.movement.analyze(
            global_tracks
        )

        # print(f"Tracks: {tracks}")
        
        people_count = self.counter.count_people(global_tracks)

        print(f"Track count: {len(global_tracks)}")
        print(f"Counter:", people_count)

        density_data = self.density.analyze(people_count)

        density = density_data["density_level"]

        occupancy_data = self.occupancy.analyze(people_count)

        occupancy = occupancy_data["occupancy_percentage"]

        congestion = self.congestion_analyzer.analyze(
            people_count=people_count,
            occupancy_percentage=occupancy,
            people_per_square_meter=density_data["people_per_square_meter"],
            average_movement=movement_stats["average_movement"]
        )

        weather = self.weather_services[camera.id].summary()

        temperature = weather["temperature"]

        humidity = weather["humidity"]

        heat = self.heat_index.reading(
            temperature,
            humidity
        )

        heat_index = heat["heat_index"]

        wind_speed = weather["wind_speed"]

        weather_code = weather["weather_code"]

        weather_desc = weather["weather_desc"]

        risk = self.risk.analyze(

            people_count=people_count,
            venue_capacity=self.density.get_capacity(),
            density=density,
            occupancy=occupancy,
            temperature=temperature,
            humidity=humidity,
            movement=movement_stats

        )

        self.trends.add(
            people_count=len(tracks),
            density=density,
            occupancy=occupancy,
            risk_score=risk["risk_score"],
            average_speed=movement_stats["average_movement"],
            moving_people=movement_stats["moving_people"],
            stationary_people=movement_stats["stationary_people"],
            flow_level=movement_stats["flow_level"]
        )

        statistics = self.statistics[camera_id]

        statistics_result = statistics.build(

            camera=self.camera_manager.info(),

            detector=self.detector.info(),

            tracker=tracker.info(),

            movement=self.movement.info(),

            feature_extractor=self.feature_extractor.info(),

            crowd_counter=self.counter.statistics(),

            density=self.density.statistics(),

            occupancy=self.occupancy.summary(),

            congestion=self.congestion_analyzer.summary(),

            trends=self.trends.summary(),

            risk=risk,

            performance=self.metrics.summary(),

            weather=weather
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

        # output = Drawing.draw_detections(
        #     output,
        #     detection_result.detections
        # )

        # output = Drawing.draw_tracks(
        #     output,
        #     tracks
        # )

        
        # ---------------------------------------
        # Statistics
        # ---------------------------------------
        # statistics = {
        #     # ======================================================
        #     # Camera Information
        #     # ======================================================
        #     "camera_id": self.camera.id,
        #     "camera_name": self.camera.name,
        #     "venue": self.camera.venue,
        #     "city": self.camera.city,
        #     "country": self.camera.country,
        #     "latitude": self.camera.latitude,
        #     "longitude": self.camera.longitude,
        #     "people_count": people_count,
        #     "occupancy": occupancy,
        #     "density": density,
        #     "temperature": temperature,
        #     "humidity": humidity,
        #     "heat_index": heat_index,
        #     "wind_speed": wind_speed,
        #     "weather_code": weather_code,
        #     "weather_desc": weather_desc,
        #     "city": self.camera.city,
        #     "country": self.camera.country,
        #     "risk_score": risk["risk_score"],
        #     "risk_level": risk["risk_level"],
        #     "detected_objects": len(detection_result.detections),
        #     "confidence": (
        #         max(obj.confidence for obj in objects)
        #         if objects else 0.0
        #     ),
        #     "processing_time":... ,
        #     "fps": float(self.metrics.average_fps())
        # }

        processing_time = time.perf_counter() - start_time
        self.metrics.record_frame(
            processing_time=processing_time,
            people_detected=people_count
        )

        # statistics["processing_time"] = processing_time    

        

        output = Drawing.render(

            frame=output,

            detections=detection_result.detections,

            tracks=tracks,

            statistics=statistics.summary(),

            fps=self.metrics.average_fps(),

            camera_name=camera.name,

            frame_number=self.metrics.frames_processed,

        )

        height, width = output.shape[:2]

        camera_payload = {
            "camera_id": camera.id,

            "camera_name": camera.name,

            "frame": output,
            "width": width,
            "height": height,
            "fps": float(self.metrics.average_fps()),
            "statistics": statistics.summary()
        }

        self.output.send_camera_frame(camera_payload)


        # Record an alert if the risk is elevated
        if risk["risk_score"] >= 70:      # choose your threshold
            self.metrics.record_alert()

        payload = DetectionRequest(
            
            camera_id=camera.id,

            camera_name=camera.name,

            venue=camera.venue,

            city=camera.city,

            country=camera.country,

            latitude=camera.latitude,

            longitude=camera.longitude,

            people_count=people_count,

            detected_objects=len(objects),

            density=density,

            occupancy=int(occupancy),

            temperature=float(temperature),

            humidity=float(humidity),

            heat_index=float(heat_index),

            wind_speed=float(wind_speed),

            weather_code=weather_code,

            weather_des=weather_desc,

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

        # payload = statistics.to_detection_request()

        # self.output.send_detection(payload)

        self.output.send_detection(payload.model_dump(mode="json"))

        # statistics_result = statistics.info()

        self.output.send_statistics(statistics_result)

        # people_count = len(tracks)

        results[camera_id] = {

            "camera": camera,

            "frame": output,

            "tracks": global_tracks,

            "detections": detection_result.detections,

            "statistics": statistics.summary(),

            "risk": risk,

            "people_count": people_count

        }

        return results

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

                results = self.process()

                for camera_id, result in results.items():

                    cv2.imshow(

                        f"Astravon Live Arena - {camera_id}",

                        result["frame"]

                    )

                key = cv2.waitKey(1)

                if key == ord("q"):
                    break

        finally:

            self.stop()

            cv2.destroyAllWindows()