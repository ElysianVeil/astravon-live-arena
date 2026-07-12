"""
============================================================
Astravon Live Arena
Validators

Purpose:
    Common validation utilities used throughout
    the backend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from backend.utils.constants import (
    MAX_CAPACITY,
    DEFAULT_TEMPERATURE,
    DEFAULT_HUMIDITY,
    # RISK_LOW,
    # RISK_MEDIUM,
    # RISK_HIGH,
    RISK_LEVELS,
    DENSITY_LEVELS
    # RISK_CRITICAL,
    # DENSITY_LOW,
    # DENSITY_MEDIUM,
    # DENSITY_HIGH,
    # DENSITY_CRITICAL
)


# ============================================================
# Capacity
# ============================================================

def validate_capacity(
    capacity: int
) -> bool:
    """
    Validates arena capacity.
    """

    return (
        0 <= capacity <= MAX_CAPACITY
    )


# ============================================================
# Occupancy
# ============================================================

def validate_occupancy(
    occupancy: int,
    capacity: int
) -> bool:
    """
    Validates occupancy.
    """

    return (
        0 <= occupancy <= capacity
    )


# ============================================================
# Temperature
# ============================================================

def validate_temperature(
    temperature: float
) -> bool:
    """
    Validates temperature.
    """

    return (
        -20.0 <= temperature <= 70.0
    )


# ============================================================
# Humidity
# ============================================================

def validate_humidity(
    humidity: float
) -> bool:
    """
    Validates humidity.
    """

    return (
        0.0 <= humidity <= 100.0
    )


# ============================================================
# Confidence
# ============================================================

def validate_confidence(
    confidence: float
) -> bool:
    """
    Validates AI confidence.
    """

    return (
        0.0 <= confidence <= 1.0
    )


# ============================================================
# Risk Score
# ============================================================

def validate_risk_score(
    score: int
) -> bool:
    """
    Validates risk score.
    """

    return (
        0 <= score <= 100
    )


# ============================================================
# Risk Level
# ============================================================

def validate_risk_level(
    risk_level: str
) -> bool:
    """
    Validates risk level.
    """

    return risk_level in RISK_LEVELS


# ============================================================
# Density
# ============================================================

def validate_density(
    density: str
) -> bool:
    """
    Validates crowd density.
    """

    return density in DENSITY_LEVELS


# ============================================================
# Heat Index
# ============================================================

def validate_heat_index(
    heat_index: float
) -> bool:
    """
    Validates heat index.
    """

    return (
        -20.0 <= heat_index <= 80.0
    )


# ============================================================
# Event Name
# ============================================================

def validate_event_name(
    name: str
) -> bool:
    """
    Validates event name.
    """

    return len(
        name.strip()
    ) >= 3


# ============================================================
# Default Environment
# ============================================================

def default_environment():
    """
    Returns default environmental values.
    """

    return {

        "temperature": DEFAULT_TEMPERATURE,

        "humidity": DEFAULT_HUMIDITY

    }