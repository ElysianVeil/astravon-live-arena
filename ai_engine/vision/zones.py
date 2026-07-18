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
        zone_type: str = "general",
        capacity: Optional[int] = None,
        color=COLOR_YELLOW,
        enabled: bool = True
    ):
        self.name = name

        self.points = np.array(
            points,
            dtype=np.int32
        )

        self.zone_type = zone_type

        self.capacity = capacity

        self.color = color

        self.enabled = enabled

        self.object_count = 0

        self.occupancy = 0.0

        self.last_updated = None

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

    def center(self) -> Tuple[int, int]:
        """
        Returns the polygon centroid.
        """

        m = cv2.moments(self.points)

        if m["m00"] == 0:
            return tuple(self.points[0])

        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])

        return (cx, cy)
    
    def area(self) -> float:
        """
        Returns polygon area.
        """

        return cv2.contourArea(self.points)
    
    def occupancy_percentage(self):

        if not self.capacity:
            return 0.0

        return min(

            100,

            (self.object_count / self.capacity) * 100
        )
    
    def density(self):

        if self.area() == 0:
            return 0

        return self.object_count / self.area()
    
    def status(self):

        if not self.capacity:
            return "UNKNOWN"

        occ = self.occupancy_percentage()

        if occ < 40:
            return "LOW"

        if occ < 70:
            return "MEDIUM"

        if occ < 90:
            return "HIGH"

        return "FULL"

    # --------------------------------------------------------
    def draw(
        self,
        frame,
        alpha=0.20
    ):
        """
        Draw zone with transparent fill.
        """

        if not self.enabled:
            return

        overlay = frame.copy()

        cv2.fillPoly(
            overlay,
            [self.points],
            self.color
        )

        frame[:] = cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1 - alpha,
            0
        )

        cv2.polylines(
            frame,
            [self.points],
            True,
            self.color,
            DEFAULT_ZONE_THICKNESS,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            self.name,
            self.center(),
            cv2.FONT_HERSHEY_SIMPLEX,
            settings.DRAW_FONT_SCALE,
            COLOR_WHITE,
            2,
            cv2.LINE_AA
        )


    def risk_level(self):

        occ = self.occupancy_percentage()

        if occ < 40:
            return "LOW"

        elif occ < 70:
            return "MEDIUM"

        elif occ < 90:
            return "HIGH"

        return "CRITICAL"

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
        name,
        points,
        zone_type="general",
        capacity=None,
        color=COLOR_YELLOW
    ):

        self.zones[name] = Zone(

            name=name,

            points=points,

            zone_type=zone_type,

            capacity=capacity,

            color=color

        )

        logger.info(f"Zone '{name}' added.")

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

    def enable_zone(
        self,
        name,
        enabled=True
    ):

        zone = self.get_zone(name)

        if zone:

            zone.enabled = enabled

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
    
    def nearest_zone(
        self,
        point
    ):

        nearest = None

        best = float("inf")

        for zone in self.zones.values():

            cx, cy = zone.center()

            dist = np.hypot(

                point[0]-cx,

                point[1]-cy

            )

            if dist < best:

                best = dist

                nearest = zone.name

        return nearest

    # --------------------------------------------------------

    def count_objects(
        self,
        detections
    ):

        counts = {

            name:0

            for name in self.zones

        }

        for zone in self.zones.values():
            zone.object_count = 0

        for detection in detections:

            center = detection.get("center")

            if center is None:
                continue

            zone_name = self.get_zone_for_point(center)

            if zone_name:

                counts[zone_name] += 1

                self.zones[zone_name].object_count += 1

        return counts
    
    def statistics(self):

        stats = {}

        for zone in self.zones.values():

            stats[zone.name] = {

                "count": zone.object_count,

                "capacity": zone.capacity,

                "occupancy": zone.occupancy_percentage(),

                "density": zone.density(),

                "status": zone.status()

            }

        return stats

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
    
    def export(self):

        return {

            name:{

                "points":zone.points.tolist(),

                "capacity":zone.capacity,

                "type":zone.zone_type,

                "color":zone.color

            }

            for name, zone in self.zones.items()

        }
    
    def import_zones(
        self,
        data
    ):

        self.clear()

        for name, z in data.items():

            self.add_zone(

                name,

                z["points"],

                zone_type=z.get("type"),

                capacity=z.get("capacity"),

                color=tuple(z.get("color", COLOR_YELLOW))

            )


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