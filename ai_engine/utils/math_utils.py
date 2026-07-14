"""
============================================================
Astravon Live Arena
Mathematical Utilities

Purpose:
    Provides reusable mathematical helper functions
    for the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import math
from statistics import mean
from typing import Iterable, Tuple


# ============================================================
# Basic Utilities
# ============================================================

def clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    """
    Restricts a value to a given range.
    """

    return max(minimum, min(value, maximum))


def percentage(
    value: float,
    total: float
) -> float:
    """
    Calculates a percentage.
    """

    if total <= 0:
        return 0.0

    return (value / total) * 100


def normalize(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    """
    Normalizes a value between 0 and 1.
    """

    if maximum == minimum:
        return 0.0

    return (value - minimum) / (maximum - minimum)


# ============================================================
# Distance Calculations
# ============================================================

def euclidean_distance(
    point1: Tuple[float, float],
    point2: Tuple[float, float]
) -> float:
    """
    Calculates the Euclidean distance
    between two points.
    """

    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )


def manhattan_distance(
    point1: Tuple[float, float],
    point2: Tuple[float, float]
) -> float:
    """
    Calculates Manhattan distance.
    """

    return (
        abs(point1[0] - point2[0]) +
        abs(point1[1] - point2[1])
    )


# ============================================================
# Bounding Boxes
# ============================================================

def bounding_box_area(
    x1: float,
    y1: float,
    x2: float,
    y2: float
) -> float:
    """
    Calculates the area of a bounding box.
    """

    width = max(0.0, x2 - x1)
    height = max(0.0, y2 - y1)

    return width * height


def bounding_box_center(
    x1: float,
    y1: float,
    x2: float,
    y2: float
) -> Tuple[float, float]:
    """
    Returns the center of a bounding box.
    """

    return (
        (x1 + x2) / 2,
        (y1 + y2) / 2
    )


# ============================================================
# Statistics
# ============================================================

def average(values: Iterable[float]) -> float:
    """
    Calculates the average value.
    """

    values = list(values)

    if not values:
        return 0.0

    return mean(values)


def maximum(values: Iterable[float]) -> float:
    """
    Returns the maximum value.
    """

    values = list(values)

    if not values:
        return 0.0

    return max(values)


def minimum(values: Iterable[float]) -> float:
    """
    Returns the minimum value.
    """

    values = list(values)

    if not values:
        return 0.0

    return min(values)


# ============================================================
# Geometry
# ============================================================

def circle_area(radius: float) -> float:
    """
    Calculates the area of a circle.
    """

    return math.pi * radius ** 2


def rectangle_area(
    width: float,
    height: float
) -> float:
    """
    Calculates rectangle area.
    """

    return width * height


# ============================================================
# Risk Calculations
# ============================================================

def weighted_average(
    values: Iterable[float],
    weights: Iterable[float]
) -> float:
    """
    Calculates a weighted average.
    """

    values = list(values)
    weights = list(weights)

    if len(values) != len(weights):
        raise ValueError(
            "Values and weights must have the same length."
        )

    total_weight = sum(weights)

    if total_weight == 0:
        return 0.0

    weighted_sum = sum(
        value * weight
        for value, weight in zip(values, weights)
    )

    return weighted_sum / total_weight


# ============================================================
# Angle Utilities
# ============================================================

def degrees_to_radians(
    angle: float
) -> float:
    """
    Converts degrees to radians.
    """

    return math.radians(angle)


def radians_to_degrees(
    angle: float
) -> float:
    """
    Converts radians to degrees.
    """

    return math.degrees(angle)


# ============================================================
# Frame Scaling
# ============================================================

def scale_value(
    value: float,
    old_min: float,
    old_max: float,
    new_min: float,
    new_max: float
) -> float:
    """
    Maps a value from one range to another.
    """

    if old_max == old_min:
        return new_min

    return (
        ((value - old_min) /
         (old_max - old_min))
        * (new_max - new_min)
        + new_min
    )


# ============================================================
# Confidence
# ============================================================

def confidence_percentage(
    confidence: float
) -> float:
    """
    Converts confidence (0-1)
    into percentage.
    """

    return round(confidence * 100, 2)