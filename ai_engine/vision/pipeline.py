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
from concurrent.futures import ThreadPoolExecutor

from config import settings
from constants import PERSON_CLASS_ID

from utils.logger import get_logger
from queue import Queue
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
from threading import Lock


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
        self.lock = Lock()

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

        self.movement = {}

        self.trends = CrowdTrends()

        self.statistics = {}

        # ======================================================
        # Runtime Cache
        # ======================================================

        self.track_cache = {}

        self.cached_weather = {}

        self.weather_last_update = {}

        self.cached_statistics = {}

        self.cached_statistics_frame = {}

        self.cached_overlay = {}

        self.cached_overlay_frame = {}

        self.frame_queue = Queue(maxsize=30)

        self.detection_queue = Queue(maxsize=30)

        self.tracking_queue = Queue(maxsize=30)

        self.reid_queue = Queue(maxsize=30)

        self.analytics_queue = Queue(maxsize=30)

        self.render_queue = Queue(maxsize=30)

        self.pipeline_executor = ThreadPoolExecutor(max_workers=8)



        self.detector = YOLODetector(
            confidence=confidence,
            model=model
        )

        self.trackers = {}

        for camera_id in self.camera_manager.cameras:

            self.trackers[camera_id] = PersonTracker()
            self.statistics[camera_id] = CrowdStatistics()
            self.movement[camera_id] = MovementAnalyzer()

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

        # Camera has already connected and detected its location
        self.camera_manager.connect_all()

        self.executor = ThreadPoolExecutor(

            max_workers=len(

                self.camera_manager.connected_cameras()

            )

        )

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

    def process(self):

        frames = self.camera_manager.read_all()

        if not frames:
            return None

        futures = []

        for camera_id, camera_data in frames.items():

            futures.append(

                self.executor.submit(

                    self.process_camera,
                    camera_id,
                    camera_data

                )

            )

        results = {}

        for future in futures:

            result = future.result()

            if result is None:
                continue

            results[result["camera"].id] = result

        return results
    
    def get_cached_weather(self, camera_id):

        return self.cached_weather.get(camera_id)
    
    def prepare_statistics(self, camera_id):

        return self.cached_statistics.get(camera_id)

    def process_track(
        self,
        track,
        frame,
        camera,
        detection_result,
        tracks
    ):

        
        print(
            track["track_id"],
            track["age"]
        )

        print("Processing track:", track["track_id"])

        x1, y1, x2, y2 = track["bbox"]

        crop = frame[y1:y2, x1:x2]
        cache_key = (

            camera.id,

            track["track_id"]

        )

        memory = self.track_cache.setdefault(cache_key,{})
        embedding = memory.get("embedding")
        w = x2 - x1
        h = y2 - y1

        if w < 60 or h < 120:
            return None

        if track["age"] % 5 == 0:

            current_frame = self.metrics.frames_processed

            needs_refresh = (

                "embedding" not in memory

                or

                current_frame - memory.get("last_update", -20) >= 20
            )

            if needs_refresh:

                embedding = self.feature_extractor.extract(crop)

                if embedding is not None:

                    memory["embedding"] = embedding

                    memory["last_update"] = current_frame

            else:

                embedding = memory["embedding"]

            print("Embedding:", embedding is not None)

        if embedding is None:
            return None

        match = self.matcher.match(
            embedding=embedding,
            camera_name=camera.name,
            camera_id=camera.id
        )
        if match is None:
            global_id = self.identity_database.register(
                embedding=embedding,
                camera_id=camera.id
            )
        else:
            global_id = match["global_id"]
            self.identity_database.update(
                global_id=global_id,
                embedding=embedding,
                camera_id=camera.id,
                bbox=track["bbox"]
            )

        print(
            f"Detections: {len(detection_result.detections)}"
        )

        print(
            f"Tracks: {len(tracks)}"
        )

        print("Global ID:", global_id)

        track["global_id"] = global_id

        track["embedding"] = embedding

        track["global_id"] = global_id
        track["embedding"] = embedding

        return track

    def process_camera(
        self,
        camera_id,
        camera_data
    ):
        start_time = time.perf_counter()

        frame = camera_data["frame"]

        camera = camera_data["camera"]

        weather = self.weather_services[camera.id]


        original_height, original_width = frame.shape[:2]

        small_frame = cv2.resize(
            frame,
            (640, 360),
            interpolation=cv2.INTER_LINEAR
        )
        t0 = time.perf_counter()

        detection_result = self.detector.detect(small_frame)

        t1 = time.perf_counter()

        objects = []

        scale_x = original_width / 640
        scale_y = original_height / 360

        for detection in detection_result.detections:

            x1, y1, x2, y2 = detection["bbox"]

            scaled_bbox = (
                round(x1 * scale_x),
                round(y1 * scale_y),
                round(x2 * scale_x),
                round(y2 * scale_y),
            )

            detection["bbox"] = scaled_bbox

            sx1, sy1, sx2, sy2 = scaled_bbox

            objects.append(
                DetectedObject(
                    label=detection["class_name"],
                    confidence=detection["confidence"],
                    x=sx1,
                    y=sy1,
                    width=sx2 - sx1,
                    height=sy2 - sy1,
                )
            )
        # ---------------------------------------
        # ByteTrack
        # ---------------------------------------
        tracker = self.trackers[camera_id]

        tracking_future = self.pipeline_executor.submit(
            tracker.update,
            detection_result.supervision
        )

        # weather_future = self.pipeline_executor.submit(
        #     self.get_cached_weather,
        #     camera.id
        # )

        # stats_future = self.pipeline_executor.submit(
        #     self.prepare_statistics,
        #     camera_id
        # )

        tracked = tracking_future.result()

        tracks = tracker.get_tracks(tracked)

        weather = self.cached_weather.get(camera.id)

        statistics_cache = self.cached_statistics.get(camera_id)

        t2 = time.perf_counter()

        # =====================================================
        # Multi-Camera ReID
        # =====================================================



        track_futures = []

        for track in tracks:

            future = self.pipeline_executor.submit(
                self.process_track,
                track,
                frame,
                camera,
                detection_result,
                tracks
            )

            track_futures.append(future)

        global_tracks = []

        for future in track_futures:

            result = future.result()

            if result is not None:
                global_tracks.append(result)

        t3 = time.perf_counter()
        movement = self.movement[camera_id]


        
        people_count = self.counter.count_people(global_tracks)

        if global_tracks:

            movement_future = self.pipeline_executor.submit(

                movement.analyze,
                global_tracks

            )

        else:
            movement_future = self.pipeline_executor.submit(

                movement.empty

            )

        density_future = self.pipeline_executor.submit(

            self.density.analyze,
            people_count

        )

        occupancy_future = self.pipeline_executor.submit(

            self.occupancy.analyze,
            people_count

        )

        print(f"Track count: {len(global_tracks)}")
        print(f"Counter:", people_count)

        movement_stats = movement_future.result()

        density_data = density_future.result()

        density = density_data["density_level"]

        occupancy_data = occupancy_future.result()

        occupancy = occupancy_data["occupancy_percentage"]

        congestion = self.congestion_analyzer.analyze(
            people_count=people_count,
            occupancy_percentage=occupancy,
            people_per_square_meter=density_data["people_per_square_meter"],
            average_movement=movement_stats["average_movement"]
        )

        now = time.time()

        weather = self.cached_weather.get(camera.id)

        if weather is None or now - self.weather_last_update.get(camera.id, 0) > 60:

            weather = self.weather_services[camera.id].summary()

            heat = self.heat_index.reading(
                weather["temperature"],
                weather["humidity"]
            )

            weather["heat_index"] = heat["heat_index"]

            self.cached_weather[camera.id] = weather
            self.weather_last_update[camera.id] = now

        temperature = weather["temperature"]
        humidity = weather["humidity"]
        heat_index = weather["heat_index"]
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

        if self.metrics.frames_processed % 5 == 0:
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

        frame_no = self.metrics.frames_processed

        if (

            camera_id not in self.cached_statistics

            or

            frame_no - self.cached_statistics_frame.get(camera_id, 0) >= 10

        ):

            self.cached_statistics[camera_id] = statistics.build(

                camera=self.camera_manager.info(),

                detector=self.detector.info(),

                tracker=tracker.info(),

                movement=movement.info(),

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

            self.cached_statistics_frame[camera_id] = frame_no

        statistics_result = self.cached_statistics[camera_id]

        t4 = time.perf_counter()

        if risk["risk_level"] in ["High", "Critical"]:
            self.output.send_alert(risk)

        logger.info(
            f"People detected: {people_count}"
        )

        # ---------------------------------------
        # Draw boxes
        # ---------------------------------------

        output = frame.copy()


        processing_time = time.perf_counter() - start_time
        with self.lock:
            self.metrics.record_frame(
                processing_time=processing_time,
                people_detected=people_count
            )
        

        if frame_no % 10 == 0:

            self.cached_overlay[camera_id] = statistics.summary()

        overlay = self.cached_overlay[camera_id]

        output = Drawing.render(

            frame=output,

            detections=detection_result.detections,

            tracks=tracks,

            statistics=overlay,

            fps=self.metrics.average_fps(),

            camera_name=camera.name,

            frame_number=self.metrics.frames_processed,

        )


        t5 = time.perf_counter()

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
            with self.lock:
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

            weather_desc=weather_desc,

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

        logger.info(
            f"""
        Detection : {(t1-t0)*1000:.1f} ms
        Tracking  : {(t2-t1)*1000:.1f} ms
        ReID      : {(t3-t2)*1000:.1f} ms
        Analytics : {(t4-t3)*1000:.1f} ms
        Drawing   : {(t5-t4)*1000:.1f} ms
        """
        )

        if frame_no % 5 == 0:
            self.output.send_detection(payload.model_dump(mode="json"))


        if frame_no % 15 == 0:
            self.output.send_statistics(statistics_result)


        return {

            "camera": camera,

            "frame": output,

            "tracks": global_tracks,

            "detections": detection_result.detections,

            "statistics": statistics.summary(),

            "risk": risk,

            "people_count": people_count

        }


    # ========================================================
    # Run Forever
    # ========================================================

    def run(self):
        """
        Starts a live AI session.
        """
        logger.info("Starting AI Engine Pipeline...")

        self.start()

        try:

            while True:

                results = self.process()

                if results is None:
                    continue

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