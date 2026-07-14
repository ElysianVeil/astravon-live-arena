"""
============================================================
Astravon Live Arena
Risk Thresholds

Purpose:
    Defines configurable thresholds used by the
    Risk Analysis Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from dataclasses import dataclass


# ============================================================
# Crowd Thresholds
# ============================================================

@dataclass(frozen=True)
class CrowdThresholds:
    """
    Crowd-related thresholds.
    """

    LOW_DENSITY: int = 30
    MEDIUM_DENSITY: int = 80
    HIGH_DENSITY: int = 120

    LOW_OCCUPANCY: float = 40.0
    MEDIUM_OCCUPANCY: float = 70.0
    HIGH_OCCUPANCY: float = 90.0


# ============================================================
# Heat Thresholds
# ============================================================

@dataclass(frozen=True)
class HeatThresholds:
    """
    Heat index thresholds (°C).
    """

    SAFE: float = 27.0
    CAUTION: float = 32.0
    DANGER: float = 41.0
    EXTREME_DANGER: float = 54.0


# ============================================================
# Risk Score Thresholds
# ============================================================

@dataclass(frozen=True)
class RiskThresholds:
    """
    Overall risk score thresholds.
    """

    LOW: int = 25
    MEDIUM: int = 50
    HIGH: int = 75
    CRITICAL: int = 90


# ============================================================
# Crowd Movement Thresholds
# ============================================================

@dataclass(frozen=True)
class MovementThresholds:
    """
    Crowd movement speed (pixels/frame or normalized units).
    """

    SLOW: float = 1.5
    NORMAL: float = 3.0
    FAST: float = 5.0


# ============================================================
# Congestion Thresholds
# ============================================================

@dataclass(frozen=True)
class CongestionThresholds:
    """
    Congestion ratio thresholds.
    """

    LOW: float = 0.30
    MEDIUM: float = 0.60
    HIGH: float = 0.85


# ============================================================
# Alert Thresholds
# ============================================================

@dataclass(frozen=True)
class AlertThresholds:
    """
    Automatic alert generation thresholds.
    """

    PEOPLE_WARNING: int = 250
    PEOPLE_CRITICAL: int = 500

    TEMPERATURE_WARNING: float = 32.0
    TEMPERATURE_CRITICAL: float = 38.0

    RISK_WARNING: int = 60
    RISK_CRITICAL: int = 85


# ============================================================
# Export Singleton Instances
# ============================================================

CROWD = CrowdThresholds()

HEAT = HeatThresholds()

RISK = RiskThresholds()

MOVEMENT = MovementThresholds()

CONGESTION = CongestionThresholds()

ALERTS = AlertThresholds()