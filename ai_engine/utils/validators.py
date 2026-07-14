"""
============================================================
Astravon Live Arena
Validators

Purpose:
    Shared validation utilities for the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


# ============================================================
# Camera Validation
# ============================================================

def validate_camera_source(source: Any) -> bool:
    """
    Validates a camera source.

    Accepts:
        - Webcam index (0, 1, 2...)
        - Video file path
        - RTSP/HTTP stream URL
    """

    if isinstance(source, int):
        return source >= 0

    if not isinstance(source, str):
        return False

    source = source.strip()

    if source.startswith(("rtsp://", "http://", "https://")):
        return True

    return Path(source).exists()


# ============================================================
# Model Validation
# ============================================================

def validate_model_path(model_path: str | Path) -> bool:
    """
    Returns True if the model exists.
    """

    return Path(model_path).exists()


# ============================================================
# Image Validation
# ============================================================

def validate_frame(frame: Any) -> bool:
    """
    Checks whether a frame is valid.
    """

    if frame is None:
        return False

    if not hasattr(frame, "shape"):
        return False

    if len(frame.shape) < 2:
        return False

    return True


# ============================================================
# Detection Validation
# ============================================================

def validate_confidence(
    confidence: float,
    minimum: float = 0.25
) -> bool:
    """
    Validates detection confidence.
    """

    return minimum <= confidence <= 1.0


def validate_people_count(count: int) -> bool:
    """
    Validates detected people count.
    """

    return count >= 0


# ============================================================
# Crowd Validation
# ============================================================

VALID_DENSITIES = {
    "Low",
    "Medium",
    "High",
    "Critical"
}


def validate_density(level: str) -> bool:
    """
    Validates crowd density.
    """

    return level in VALID_DENSITIES


# ============================================================
# Heat Validation
# ============================================================

def validate_temperature(
    temperature: float
) -> bool:
    """
    Validates temperature.
    """

    return -30.0 <= temperature <= 70.0


def validate_humidity(
    humidity: float
) -> bool:
    """
    Validates humidity.
    """

    return 0.0 <= humidity <= 100.0


def validate_heat_index(
    heat_index: float
) -> bool:
    """
    Validates heat index.
    """

    return -30.0 <= heat_index <= 90.0


# ============================================================
# Risk Validation
# ============================================================

def validate_risk_score(
    score: int
) -> bool:
    """
    Risk score must be between 0 and 100.
    """

    return 0 <= score <= 100


VALID_SEVERITIES = {
    "Low",
    "Medium",
    "High",
    "Critical"
}


def validate_severity(
    severity: str
) -> bool:
    """
    Validates risk severity.
    """

    return severity in VALID_SEVERITIES


# ============================================================
# Bounding Boxes
# ============================================================

def validate_bbox(
    x1: float,
    y1: float,
    x2: float,
    y2: float
) -> bool:
    """
    Validates bounding box coordinates.
    """

    return (
        x1 >= 0
        and y1 >= 0
        and x2 > x1
        and y2 > y1
    )


# ============================================================
# Generic Validation
# ============================================================

def validate_non_empty(value: str) -> bool:
    """
    Checks if a string is not empty.
    """

    return bool(value and value.strip())


def validate_positive(value: float | int) -> bool:
    """
    Checks whether a number is positive.
    """

    return value >= 0


def validate_percentage(value: float) -> bool:
    """
    Checks percentage range.
    """

    return 0.0 <= value <= 100.0


# ============================================================
# Event Validation
# ============================================================

def validate_event_name(name: str) -> bool:
    """
    Validates an event name.
    """

    return (
        isinstance(name, str)
        and len(name.strip()) >= 3
    )


# ============================================================
# Report Validation
# ============================================================

def validate_report(report: dict) -> bool:
    """
    Validates report structure.
    """

    required_fields = (
        "event_name",
        "statistics",
        "alerts"
    )

    return all(
        field in report
        for field in required_fields
    )