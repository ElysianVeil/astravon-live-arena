"""
============================================================
Astravon Live Arena
Helper Utilities

Purpose:
    Provides reusable helper functions used across
    the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================
# Time Utilities
# ============================================================

def current_timestamp() -> str:
    """
    Returns the current UTC timestamp.
    """

    return datetime.utcnow().isoformat()


def current_datetime() -> datetime:
    """
    Returns the current datetime.
    """

    return datetime.utcnow()


def current_time_ms() -> int:
    """
    Returns the current time in milliseconds.
    """

    return int(time.time() * 1000)


# ============================================================
# ID Utilities
# ============================================================

def generate_id() -> str:
    """
    Generates a unique identifier.
    """

    return str(uuid.uuid4())


# ============================================================
# File Utilities
# ============================================================

def ensure_directory(path: str | Path) -> Path:
    """
    Creates a directory if it does not exist.
    """

    directory = Path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return directory


def file_exists(path: str | Path) -> bool:
    """
    Returns True if a file exists.
    """

    return Path(path).exists()


# ============================================================
# Number Utilities
# ============================================================

def clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    """
    Restricts a value within a range.
    """

    return max(
        minimum,
        min(value, maximum)
    )


def percentage(
    value: float,
    total: float
) -> float:
    """
    Calculates a percentage.
    """

    if total <= 0:
        return 0.0

    return round(
        (value / total) * 100,
        2
    )


# ============================================================
# Dictionary Utilities
# ============================================================

def merge_dicts(
    *dictionaries: dict
) -> dict:
    """
    Merges multiple dictionaries.
    """

    merged = {}

    for dictionary in dictionaries:
        merged.update(dictionary)

    return merged


# ============================================================
# Frame Utilities
# ============================================================

def frame_size(frame: Any) -> tuple[int, int]:
    """
    Returns frame width and height.
    """

    height, width = frame.shape[:2]

    return width, height


def frame_center(frame: Any) -> tuple[int, int]:
    """
    Returns the center of a frame.
    """

    width, height = frame_size(frame)

    return (
        width // 2,
        height // 2
    )


# ============================================================
# Formatting
# ============================================================

def format_duration(
    seconds: float
) -> str:
    """
    Formats seconds into HH:MM:SS.
    """

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(seconds % 60)

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d}"
    )


# ============================================================
# Serialization
# ============================================================

def object_to_dict(obj: Any) -> dict:
    """
    Converts an object into a dictionary.
    """

    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    if hasattr(obj, "__dict__"):
        return vars(obj)

    return {}


# ============================================================
# Retry Helper
# ============================================================

def retry(
    function,
    retries: int = 3,
    delay: float = 1.0,
    *args,
    **kwargs
):
    """
    Retries a function several times.
    """

    last_exception = None

    for _ in range(retries):

        try:

            return function(
                *args,
                **kwargs
            )

        except Exception as error:

            last_exception = error

            time.sleep(delay)

    raise last_exception