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

        self.detect_every = 4
        self.frame_counter = 0

        # Cached detection used on skipped frames
        self.cached_result = None

        # --------------------------------------------------------
        # PyTorch Optimizations
        # --------------------------------------------------------

        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = True

        logger.info("Warming up YOLO model...")

        dummy = np.zeros(
            (640, 640, 3),
            dtype=np.uint8
        )

        with torch.inference_mode():

            with torch.autocast(
                device_type="cuda",
                enabled=torch.cuda.is_available()
            ):

                self.model.predict(
                    source=dummy,
                    imgsz=416,
                    verbose=False
                )

        logger.info("YOLO warm-up complete.")


        logger.info(

            f"Using device: "

            f"{'CUDA' if torch.cuda.is_available() else 'CPU'}"

        )
        if torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True

            torch.set_float32_matmul_precision("high")

            try:

                self.model.model.half()

                try:
                    self.model.model = torch.compile(
                        self.model.model,
                        mode="reduce-overhead"
                    )

                    logger.info("Torch Compile enabled.")

                except Exception:

                    logger.warning(
                        "Torch Compile unavailable."
                    )

                logger.info("FP16 inference enabled.")

            except Exception:

                logger.warning(
                    "FP16 not supported."
                )

        self.labels = loader.labels

        self.use_supervision = True

        self.confidence = confidence

        self.class_names = self.model.names


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
        
        self.frame_counter += 1

        # --------------------------------------------------------
        # Adaptive Detection Rate
        # --------------------------------------------------------

        if self.cached_result is not None:

            people = len(self.cached_result.detections)

            if people < 5:

                self.detect_every = 8

            elif people < 20:

                self.detect_every = 5

            else:

                self.detect_every = 2

        # Skip inference and reuse the previous detection
        if (
            self.frame_counter % self.detect_every != 0
            and self.cached_result is not None
        ):
            return self.cached_result

        logger.debug("Running YOLO inference.")

        start = time.perf_counter()

        with torch.inference_mode():

            with torch.autocast(
                device_type="cuda",
                enabled=torch.cuda.is_available()
            ):

                result = self.model.predict(
                    source=frame,
                    imgsz=416,
                    conf=self.confidence,
                    classes=list(self.allowed_classes),
                    verbose=False,
                    save=False,
                    show=False
                )[0]
        elapsed = time.perf_counter() - start

        self.processing_time = elapsed
        self.total_processing_time += elapsed
        self.frames_processed += 1
        self.last_result = result

        if self.use_supervision:
            sv_detections = sv.Detections.from_ultralytics(result)
        else:
            sv_detections=None

        detections = []

        if result.boxes is not None:

            # Transfer all detections from GPU to CPU only once
            boxes = result.boxes.cpu()

            for box in boxes:

                bbox = box.xyxy[0].numpy().astype(np.int32)

                x1, y1, x2, y2 = bbox.tolist()

                class_id = int(box.cls.item())

                confidence = float(box.conf.item())

                detections.append({
                    "class_id": class_id,
                    "class_name": self.class_names[class_id],
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })


        self.last_detection_time = time.time()

        self.total_detections += len(detections)

        summary = {}

        for d in detections:
            name = d["class_name"]
            summary[name] = summary.get(name,0)+1

        summary_text = ", ".join(
            f"{name}: {count}"
            for name, count in summary.items()
        )

        if self.frames_processed % 30 == 0:

            logger.info(

                f"Detected -> {summary_text or 'None'} | "

                f"{elapsed * 1000:.2f} ms | "

                f"{1 / elapsed:.1f} FPS"

            )

        self.last_result = DetectionResult(
            timestamp=time.time(),

            ultralytics=result,

            supervision=sv_detections,

            detections=detections

        )

        self.cached_result = self.last_result

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

            imgsz=416,

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