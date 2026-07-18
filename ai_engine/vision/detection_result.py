"""
============================================================
Astravon Live Arena
Detection Result

Purpose:
    Stores all outputs produced by the YOLO detector
    after a single inference.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
from datetime import datetime

import supervision as sv


@dataclass(slots=True)
class DetectionResult:
    """
    Complete output of one YOLO inference.
    """
    timestamp: datetime

    # Raw Ultralytics result
    ultralytics: Any

    # Supervision detections
    supervision: sv.Detections

    # Project-friendly detections
    detections: List[Dict]