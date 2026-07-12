"""
============================================================
Astravon Live Arena
Helpers

Purpose:
    Common helper functions used throughout
    the backend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime

from backend.utils.constants import (
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    RISK_CRITICAL,

    DENSITY_LOW,
    DENSITY_MEDIUM,
    DENSITY_HIGH,
    DENSITY_CRITICAL
)


# ============================================================
# Timestamp
# ============================================================

def current_timestamp() -> datetime:
    """
    Returns the current UTC timestamp.
    """

    return datetime.utcnow()


# ============================================================
# Occupancy Percentage
# ============================================================

def calculate_occupancy(
    people_count: int,
    capacity: int
) -> float:
    """
    Calculates occupancy percentage.
    """

    if capacity <= 0:

        return 0.0

    return round(
        (people_count / capacity) * 100,
        2
    )


# ============================================================
# Heat Index (Simple)
# ============================================================

def calculate_heat_index(
    temperature: float,
    humidity: float
) -> float:
    """
    Simple heat index estimation.
    """

    return round(
        temperature + (humidity * 0.05),
        2
    )


# ============================================================
# Risk Level
# ============================================================

def calculate_risk_level(
    score: int
) -> str:
    """
    Converts a risk score into a risk level.
    """

    if score >= 80:

        return RISK_CRITICAL

    if score >= 60:

        return RISK_HIGH

    if score >= 40:

        return RISK_MEDIUM

    return RISK_LOW


# ============================================================
# Density
# ============================================================

def calculate_density(
    occupancy: float
) -> str:
    """
    Determines crowd density.
    """

    if occupancy >= 90:

        return DENSITY_CRITICAL

    if occupancy >= 70:

        return DENSITY_HIGH

    if occupancy >= 40:

        return DENSITY_MEDIUM

    return DENSITY_LOW


# ============================================================
# Percentage
# ============================================================

def percentage(
    value: float,
    total: float
) -> float:
    """
    Calculates a percentage.
    """

    if total == 0:

        return 0.0

    return round(
        (value / total) * 100,
        2
    )


# ============================================================
# Response Time
# ============================================================

def format_response_time(
    seconds: float
) -> str:
    """
    Formats seconds into a readable string.
    """

    return f"{seconds:.2f} sec"


# ============================================================
# Generate File Name
# ============================================================

def generate_report_filename(
    report_type: str
) -> str:
    """
    Generates a report filename.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report = report_type.lower().replace(
        " ",
        "_"
    )

    return f"{report}_{timestamp}.json"


# ============================================================
# Safe Integer
# ============================================================

def safe_int(
    value,
    default: int = 0
) -> int:
    """
    Safely converts a value to an integer.
    """

    try:

        return int(value)

    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# Safe Float
# ============================================================

def safe_float(
    value,
    default: float = 0.0
) -> float:
    """
    Safely converts a value to a float.
    """

    try:

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# System Uptime
# ============================================================

def uptime(
    start_time: datetime
) -> str:
    """
    Returns application uptime.
    """

    delta = datetime.utcnow() - start_time

    return str(delta).split(".")[0]