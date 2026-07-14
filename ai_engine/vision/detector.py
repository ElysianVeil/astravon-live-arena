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

        self.model = loader.load()
        self.labels = loader.labels

        self.confidence = confidence

        self.classes = classes

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

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            classes=self.classes,
            verbose=False
        )
        result = results[0]

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

                detections.append({

                    "class_id": int(box.cls[0]),

                    "class_name": self.model.names[
                        int(box.cls[0])
                    ],

                    "confidence": float(box.conf[0]),

                    "bbox": [x1, y1, x2, y2]

                })

        logger.info(
            f"Detected {len(detections)} objects."
        )

        return DetectionResult(

            ultralytics=result,

            supervision=sv_detections,

            detections=detections

        )

    # ========================================================
    # Person Detection
    # ========================================================

    def detect_people(
        self,
        frame: np.ndarray
    ) -> List[Dict]:
        """
        Detects only people.

        YOLO class 0 = person.
        """

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            classes=[PERSON_CLASS_ID],
            verbose=False
        )

        people: List[Dict] = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                    .astype(int)
                )

                people.append(
                    {
                        "confidence": float(box.conf[0]),
                        "bbox": [
                            x1,
                            y1,
                            x2,
                            y2
                        ]
                    }
                )

        return people

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

        return len([
            d
            for d in self.detect(frame)
            if d["class_id"] == class_id
        ])

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