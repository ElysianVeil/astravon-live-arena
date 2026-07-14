"""
============================================================
Astravon Live Arena
Vision Zones

Purpose:
    Defines polygon-based monitoring zones for
    crowd analysis, occupancy, and incident detection.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

from config import settings
from constants import (
    COLOR_YELLOW,
    COLOR_WHITE,
    DEFAULT_ZONE_THICKNESS,
)
from utils.logger import get_logger


# ============================================================
# Zone
# ============================================================
logger = get_logger("Zones")

class Zone:
    """
    Represents a monitoring zone.

    Example:
        Entrance
        Exit
        VIP Area
        Field
        Emergency Gate
    """

    def __init__(
        self,
        name: str,
        points: List[Tuple[int, int]],
        zone_type="general",
        capacity=None
    ):
        self.name = name
        self.points = np.array(
            points,
            dtype=np.int32
        )

    # --------------------------------------------------------

    def contains(
        self,
        point: Tuple[int, int]
    ) -> bool:
        """
        Returns True if the point lies inside the zone.
        """

        result = cv2.pointPolygonTest(
            self.points,
            point,
            False
        )

        return result >= 0

    # --------------------------------------------------------

    def draw(
        self,
        frame,
        color=COLOR_YELLOW,
        thickness=DEFAULT_ZONE_THICKNESS
    ):
        """
        Draw the zone polygon.
        """

        cv2.polylines(
            frame,
            [self.points],
            isClosed=True,
            color=color,
            thickness=thickness
        )

        x, y = self.points[0]

        cv2.putText(
            frame,
            self.name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )


# ============================================================
# Zone Manager
# ============================================================

class ZoneManager:
    """
    Stores and manages all zones.
    """

    def __init__(self):

        self.zones: Dict[str, Zone] = {}

    # --------------------------------------------------------

    def add_zone(
        self,
        name: str,
        points: List[Tuple[int, int]]
    ):
        """
        Register a new zone.
        """
        logger.info(f"Zone '{name}' added.")

        self.zones[name] = Zone(
            name,
            points
        )

    # --------------------------------------------------------

    def remove_zone(
        self,
        name: str
    ):
        """
        Remove a zone.
        """
        logger.info(f"Zone '{name}' removed.")

        self.zones.pop(name, None)

    # --------------------------------------------------------

    def get_zone(
        self,
        name: str
    ) -> Optional[Zone]:
        """
        Retrieve a zone.
        """

        return self.zones.get(name)

    # --------------------------------------------------------

    def draw(
        self,
        frame
    ):
        """
        Draw all zones.
        """

        for zone in self.zones.values():
            zone.draw(frame)

    # --------------------------------------------------------

    def get_zone_for_point(
        self,
        point: Tuple[int, int]
    ) -> Optional[str]:
        """
        Returns the name of the zone
        containing the point.
        """

        for zone in self.zones.values():

            if zone.contains(point):
                return zone.name

        return None

    # --------------------------------------------------------

    def count_objects(
        self,
        detections: List[dict]
    ) -> Dict[str, int]:
        """
        Counts detections inside each zone.

        Expected detection format:

        {
            "center": (x, y)
        }
        """

        counts = {
            name: 0
            for name in self.zones
        }

        for detection in detections:

            center = detection.get("center")

            if center is None:
                continue

            zone_name = self.get_zone_for_point(center)

            if zone_name:
                counts[zone_name] += 1

        return counts

    # --------------------------------------------------------

    def clear(self):
        """
        Removes all zones.
        """
        logger.info("All monitoring zones cleared.")

        self.zones.clear()

    # --------------------------------------------------------

    def list_zones(self) -> List[str]:
        """
        Returns registered zone names.
        """

        return list(self.zones.keys())


# ============================================================
# Default Zones
# ============================================================

def create_default_zones() -> ZoneManager:
    """
    Creates sample monitoring zones.

    Coordinates assume a 1280x720 frame.
    """

    manager = ZoneManager()

    manager.add_zone(
        "Entrance",
        [
            (20, 200),
            (250, 200),
            (250, 600),
            (20, 600)
        ]
    )

    manager.add_zone(
        "Field",
        [
            (300, 120),
            (980, 120),
            (980, 620),
            (300, 620)
        ]
    )

    manager.add_zone(
        "Emergency Exit",
        [
            (1030, 200),
            (1260, 200),
            (1260, 600),
            (1030, 600)
        ]
    )

    return manager