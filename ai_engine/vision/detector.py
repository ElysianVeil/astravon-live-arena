"""
============================================================
Astravon Live Arena
YOLO Detector

Purpose:
    Performs object detection using a pretrained
    Ultralytics YOLO model.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Dict, List, Optional

import cv2
import numpy as np
import time
import torch
from collections import deque
from collections import Counter

from config import settings
from constants import PERSON_CLASS_ID
from models.yolov_model.loader import loader
from utils.logger import get_logger
from utils.validators import validate_frame
from vision.drawing import Drawing
from vision.detection_result import DetectionResult
import supervision as sv

# ============================================================
# YOLO Detector
# ============================================================

logger = get_logger("Detector")

class YOLODetector:
    """
    Wrapper around the Ultralytics YOLO model.
    """


    def __init__(
        self,
        model,
        confidence: float = settings.CONFIDENCE_THRESHOLD,
        classes: Optional[List[int]] = None
    ):
        """
        Args:
            confidence:
                Minimum confidence threshold.

            classes:
                YOLO class IDs to detect.
                None = detect every class.
                [0] = detect only people.
        """

        self.model = model

        logger.info("Warming up YOLO model...")

        dummy = np.zeros(
            (640, 640, 3),
            dtype=np.uint8
        )

        self.model.predict(
            source=dummy,
            verbose=False
        )

        logger.info("YOLO warm-up complete.")


        logger.info(

            f"Using device: "

            f"{'CUDA' if torch.cuda.is_available() else 'CPU'}"

        )
        if torch.cuda.is_available():

            try:

                self.model.model.half()

                logger.info("FP16 inference enabled.")

            except Exception:

                logger.warning(
                    "FP16 not supported."
                )

        self.labels = loader.labels

        self.confidence = confidence


        self.frames_processed = 0
        self.total_detections = 0
        self.processing_time = 0.0
        self.total_processing_time = 0.0
        self.last_result = None
        self.history = deque(maxlen=50)
        self.last_detection_time = None

        # Classes that will be kept after inference.
        # None = keep every detected class.
        self.allowed_classes = (
            set(classes)
            if classes is not None
            else {0, 2, 5}
        )
    # ========================================================
    # Detection
    # ========================================================

    def detect(
        self,
        frame: np.ndarray
    ) -> List[Dict]:
        """
        Runs YOLO detection.

        Returns:
            List of detections.
        """

        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return []

        logger.debug("Running YOLO inference.")

        start = time.perf_counter()

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False
        )
        result = results[0]
        elapsed = time.perf_counter() - start

        self.processing_time = elapsed
        self.total_processing_time += elapsed
        self.frames_processed += 1
        self.last_result = result

        sv_detections = sv.Detections.from_ultralytics(result)

        detections = []

        if result.boxes is not None:

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                    .astype(int)
                )

                if float(box.conf[0]) < self.confidence:
                    continue

                class_id = int(box.cls[0])

                if (
                    self.allowed_classes is not None
                    and class_id not in self.allowed_classes
                ):                   
                    continue

                detections.append({

                    "class_id": class_id,

                    "class_name": self.model.names[
                        int(box.cls[0])
                    ],

                    "confidence": float(box.conf[0]),

                    "bbox": [x1, y1, x2, y2]

                })

            self.last_detection_time = time.time()

            self.total_detections += len(detections)

        counts = Counter(
            d["class_name"]
            for d in detections
        )

        summary = ", ".join(
            f"{name}: {count}"
            for name, count in counts.items()
        )

        logger.info(

            f"Detected -> {summary or 'None'} | "

            f"{elapsed * 1000:.2f} ms | "

            f"{1 / elapsed:.1f} FPS"

        )

        self.last_result = DetectionResult(
            timestamp=time.time(),

            ultralytics=result,

            supervision=sv_detections,

            detections=detections

        )

        self.history.append(self.last_result)

        return self.last_result
    
    def get_latest_detection(self):

       return self.last_result
    
    def detect_batch(
        self,
        frames: List[np.ndarray]
    ):

        if not frames:
            return []

        return self.model.predict(

            source=frames,

            conf=self.confidence,

            verbose=False

        )
    
    @property
    def fps(self):

        if self.processing_time == 0:
            return 0

        return 1 / self.processing_time

    @property
    def average_processing_time(self):

        if self.frames_processed == 0:
            return 0

        return (

            self.total_processing_time

            /

            self.frames_processed

        )
    
    # ========================================================
    # Person Detection
    # ========================================================

    def detect_people(self, frame):

        result = self.detect(frame)

        return [

            d

            for d in result.detections

            if d["class_id"] == PERSON_CLASS_ID

        ]

    # ========================================================
    # Count
    # ========================================================

    def count(
        self,
        frame,
        class_id: int
    ) -> int:
        """
        Returns the number of detected people.
        """

        result = self.detect(frame)

        return len(

            [

                d

                for d in result.detections

                if d["class_id"] == class_id

            ]

        )
    
    # ========================================================
    # Drawing
    # ========================================================

    def draw(
        self,
        frame,
        detections
    ):
        return Drawing.draw_detections(
            frame,
            detections
        )
    
    def model_info(self):

        return loader.model_info()
    
    @property
    def ready(self):

        return loader.loaded
    
    def info(self):
        model = self.model_info()

        return {

            "model": model["model_name"],

            "ready": self.ready,

            "frames_processed":

                self.frames_processed,

            "total_detections":

                self.total_detections,

            "processing_time_ms":

                round(

                    self.processing_time*1000,

                    2

                ),

            "average_processing_time_ms":

                round(

                    self.average_processing_time*1000,

                    2

                ),

            "class_filter": self.class_filter,

            "last_detection_time":

                self.last_detection_time,

            "fps":

                round(

                    self.fps,

                    2

                )

        }
    
    def set_allowed_classes(self, classes: List[int] | None):
        """
        Update the class filter.

        None = detect every class.
        """

        self.allowed_classes = (
            set(classes)
            if classes is not None
            else None
        )


    def add_class(self, class_id: int):
        """
        Add a class to the filter.
        """

        if self.allowed_classes is None:
            self.allowed_classes = set()

        self.allowed_classes.add(class_id)


    def remove_class(self, class_id: int):
        """
        Remove a class from the filter.
        """

        if self.allowed_classes is not None:
            self.allowed_classes.discard(class_id)


    @property
    def class_filter(self):
        """
        Returns the active class filter.
        """

        if self.allowed_classes is None:
            return "All"

        return sorted(self.allowed_classes)