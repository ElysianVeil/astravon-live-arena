"""
============================================================
Astravon Live Arena
Drawing Utilities

Purpose:
    Draws detections, tracked people, statistics,
    zones, and alerts on video frames.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import cv2
import numpy as np
from datetime import datetime
import time

from config import settings
from constants import (
    COLOR_RED,
    COLOR_YELLOW,
    COLOR_ORANGE,
    COLOR_GREEN,
    COLOR_WHITE,
)
from utils.logger import get_logger

# --------------------------------------------------------
# OpenCV Optimizations
# --------------------------------------------------------

cv2.setUseOptimized(True)
cv2.setNumThreads(0)

# ============================================================
# Drawing
# ============================================================

logger = get_logger("Drawing")

class Drawing:

    # --------------------------------------------------------
    # Drawing Metrics
    # --------------------------------------------------------

    frames_drawn = 0
    current_draw_time = 0.0
    total_draw_time = 0.0
    # --------------------------------------------------------
    # Bounding Boxes
    # --------------------------------------------------------

    @staticmethod
    def draw_detection(
        frame: np.ndarray,
        bbox: List[int],
        label: str,
        confidence: float,
        color: Tuple[int, int, int] | None = None
    ) -> np.ndarray:
        """
        Draws one detection.
        """
        if color is None:
            if confidence >= 0.90:
                color = COLOR_GREEN
            elif confidence >= 0.75:
                color = COLOR_YELLOW
            elif confidence >= 0.50:
                color = COLOR_ORANGE
            else:
                color = COLOR_RED

        x1, y1, x2, y2 = bbox

        scale = max(frame.shape[1] / 1280, 0.6)

        font_scale = 0.6 * scale

        thickness = max(2, int(scale * 2))

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            thickness, 
            lineType=cv2.LINE_AA
        )

        text = f"{label} {confidence:.2f}"

        (text_width, text_height), _ = cv2.getTextSize(
            text,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            thickness
        )

        cv2.rectangle(
            frame,
            (x1, y1 - 28),
            (x1 + text_width + 8, y1),
            color,
            -1, 
            lineType=cv2.LINE_AA
        )

        cv2.putText(
            frame,
            text,
            (x1 + 4, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            COLOR_WHITE,
            thickness, 
            lineType=cv2.LINE_AA
        )

        return frame
    
    # --------------------------------------------------------
    # Detection Centre
    # --------------------------------------------------------

    @staticmethod
    def draw_center(
        frame: np.ndarray,
        bbox: List[int],
        color: Tuple[int, int, int] = COLOR_GREEN
    ) -> np.ndarray:
        """
        Draws the centre point of a bounding box.
        """

        x1, y1, x2, y2 = bbox

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        cv2.circle(
            frame,
            (cx, cy),
            4,
            color,
            -1, 
            lineType=cv2.LINE_AA
        )

        return frame

    @staticmethod
    def draw_detections(
        frame,
        detections
    ):

        for detection in detections:

            Drawing.draw_detection(
                frame,
                detection["bbox"],
                detection["class_name"],
                detection["confidence"]
            )

        return frame
    
    # --------------------------------------------------------
    # Rounded Bounding Box
    # --------------------------------------------------------

    @staticmethod
    def draw_rounded_box(
        frame: np.ndarray,
        bbox: List[int],
        color: Tuple[int, int, int] = COLOR_GREEN,
        thickness: int = 2,
        radius: int = 8
    ) -> np.ndarray:
        """
        Draws a rounded rectangle.
        """

        x1, y1, x2, y2 = bbox

        # Horizontal
        cv2.line(frame, (x1 + radius, y1), (x2 - radius, y1), color, thickness, lineType=cv2.LINE_AA)
        cv2.line(frame, (x1 + radius, y2), (x2 - radius, y2), color, thickness, lineType=cv2.LINE_AA)

        # Vertical
        cv2.line(frame, (x1, y1 + radius), (x1, y2 - radius), color, thickness, lineType=cv2.LINE_AA)
        cv2.line(frame, (x2, y1 + radius), (x2, y2 - radius), color, thickness, lineType=cv2.LINE_AA)

        # Corners
        cv2.ellipse(frame, (x1 + radius, y1 + radius),
                    (radius, radius), 180, 0, 90,
                    color, thickness)

        cv2.ellipse(frame, (x2 - radius, y1 + radius),
                    (radius, radius), 270, 0, 90,
                    color, thickness)

        cv2.ellipse(frame, (x1 + radius, y2 - radius),
                    (radius, radius), 90, 0, 90,
                    color, thickness)

        cv2.ellipse(frame, (x2 - radius, y2 - radius),
                    (radius, radius), 0, 0, 90,
                    color, thickness)

        return frame

    # --------------------------------------------------------
    # Tracks
    # --------------------------------------------------------

    @staticmethod
    def draw_track(
        frame: np.ndarray,
        track: Dict
    ) -> np.ndarray:
        """
        Draws one tracked person.
        """

        x1, y1, x2, y2 = track["bbox"]

        track_id = track["track_id"]

        color = (255, 180, 0)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2, 
            lineType=cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"Person {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2, 
            lineType=cv2.LINE_AA
        )

        return frame
    
    # --------------------------------------------------------
    # Track Trail
    # --------------------------------------------------------

    @staticmethod
    def draw_trail(
        frame: np.ndarray,
        points: List[Tuple[int, int]],
        color: Tuple[int, int, int] = (255, 180, 0)
    ) -> np.ndarray:
        """
        Draws the movement trail of a tracked object.
        """

        if len(points) < 2:
            return frame

        for i in range(1, len(points)):
            cv2.line(
                frame,
                points[i - 1],
                points[i],
                color,
                2, 
                lineType=cv2.LINE_AA
            )

        return frame

    # --------------------------------------------------------
    # Multiple Tracks
    # --------------------------------------------------------

    @staticmethod
    def draw_tracks(
        frame: np.ndarray,
        tracks: List[Dict]
    ) -> np.ndarray:
        """
        Draws every tracked person.
        """

        for track in tracks:
            Drawing.draw_track(
                frame,
                track
            )

        return frame

    # --------------------------------------------------------
    # Statistics Panel
    # --------------------------------------------------------

    @staticmethod
    def draw_statistics(
        frame: np.ndarray,
        people_count: int,
        density: str,
        occupancy: float,
        temperature: float,
        risk_score: int
    ) -> np.ndarray:
        """
        Draws statistics.
        """

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (10,10),
            (270,185),
            (0,0,0),
            -1, 
            lineType=cv2.LINE_AA
        )

        frame = cv2.addWeighted(
            overlay,
            0.35,
            frame,
            0.65,
            0
        )

        lines = [
            f"People: {people_count}",
            f"Density: {density}",
            f"Occupancy: {occupancy:.2f}%",
            f"Temperature: {temperature:.1f} C",
            f"Risk Score: {risk_score}"
        ]

        x = 20
        y = 20

        for line in lines:

            cv2.putText(
                frame,
                line,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2, 
                lineType=cv2.LINE_AA
            )

            y += 30

        return frame
    
    # --------------------------------------------------------
    # Risk Indicator
    # --------------------------------------------------------

    @staticmethod
    def draw_risk_indicator(
        frame: np.ndarray,
        score: float
    ) -> np.ndarray:
        """
        Draws a coloured risk indicator.
        """

        if score >= 90:
            text = "CRITICAL"
            color = COLOR_RED

        elif score >= 70:
            text = "HIGH"
            color = COLOR_ORANGE

        elif score >= 40:
            text = "MEDIUM"
            color = COLOR_YELLOW

        else:
            text = "LOW"
            color = COLOR_GREEN

        x = 20
        y = 200

        cv2.rectangle(
            frame,
            (x - 5, y - 22),
            (x + 170, y + 10),
            color,
            -1, 
            lineType=cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"Risk: {text}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            COLOR_WHITE,
            2, 
            lineType=cv2.LINE_AA
        )

        return frame

    # --------------------------------------------------------
    # Alert
    # --------------------------------------------------------

    @staticmethod
    def draw_alert(
        frame: np.ndarray,
        title: str,
        severity: str
    ) -> np.ndarray:
        """
        Displays an alert banner.
        """

        color = (0, 255, 255)

        if severity.lower() == "medium":
            color = (0, 165, 255)

        elif severity.lower() == "high":
            color = (0, 0, 255)

        cv2.rectangle(
            frame,
            (0, 0),
            (frame.shape[1], 45),
            color,
            -1, 
            lineType=cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"{severity.upper()} : {title}",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2, 
            lineType=cv2.LINE_AA
        )

        return frame

    # --------------------------------------------------------
    # FPS
    # --------------------------------------------------------

    @staticmethod
    def draw_fps(
        frame: np.ndarray,
        fps: float
    ) -> np.ndarray:
        """
        Displays FPS.
        """

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2, 
            lineType=cv2.LINE_AA
        )

        return frame

    # --------------------------------------------------------
    # Camera Name
    # --------------------------------------------------------

    @staticmethod
    def draw_camera_name(
        frame: np.ndarray,
        camera_name: str
    ) -> np.ndarray:
        """
        Displays the camera name.
        """

        cv2.putText(
            frame,
            camera_name,
            (frame.shape[1] - 220, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2, 
            lineType=cv2.LINE_AA
        )

        return frame

    # --------------------------------------------------------
    # Crosshair
    # --------------------------------------------------------

    @staticmethod
    def draw_crosshair(
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Draws a centre crosshair.
        """

        h, w = frame.shape[:2]

        cx = w // 2
        cy = h // 2

        cv2.line(
            frame,
            (cx - 20, cy),
            (cx + 20, cy),
            (0, 255, 255),
            2,
            lineType=cv2.LINE_AA
        )

        cv2.line(
            frame,
            (cx, cy - 20),
            (cx, cy + 20),
            (0, 255, 255),
            2,
            lineType=cv2.LINE_AA
        )

        return frame
    
    # --------------------------------------------------------
    # Zone Drawing
    # --------------------------------------------------------

    @staticmethod
    def draw_zone(
        frame: np.ndarray,
        polygon: List[Tuple[int, int]],
        name: str,
        color: Tuple[int, int, int] = COLOR_GREEN
    ) -> np.ndarray:
        """
        Draws a named polygon zone.
        """

        pts = np.array(
            polygon,
            dtype=np.int32
        )

        overlay = frame.copy()

        cv2.fillPoly(
            overlay,
            [pts],
            color
        )

        frame = cv2.addWeighted(
            overlay,
            0.20,
            frame,
            0.80,
            0
        )

        cv2.polylines(
            frame,
            [pts],
            True,
            color,
            2, 
            lineType=cv2.LINE_AA
        )

        x, y = pts[0]

        cv2.putText(
            frame,
            name,
            (x, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2, 
            lineType=cv2.LINE_AA
        )

        return frame
        
   # --------------------------------------------------------
    # Heatmap Overlay
    # --------------------------------------------------------

    @staticmethod
    def draw_heatmap(
        frame: np.ndarray,
        heatmap: np.ndarray
    ) -> np.ndarray:
        """
        Overlays a heatmap onto the frame.
        """

        if heatmap is None:
            return frame

        if heatmap.shape[:2] != frame.shape[:2]:
            heatmap = cv2.resize(
                heatmap,
                (frame.shape[1], frame.shape[0])
            )

        if heatmap.dtype != np.uint8:
            heatmap = cv2.normalize(
                heatmap,
                None,
                0,
                255,
                cv2.NORM_MINMAX
            ).astype(np.uint8)

        maps = {

            "JET": cv2.COLORMAP_JET,

            "HOT": cv2.COLORMAP_HOT,

            "INFERNO": cv2.COLORMAP_INFERNO,

            "PLASMA": cv2.COLORMAP_PLASMA,

            "VIRIDIS": cv2.COLORMAP_VIRIDIS

        }

        overlay = cv2.applyColorMap(

            heatmap,

            maps.get(

                settings.HEATMAP_MODE,

                cv2.COLORMAP_JET

            )

        )
        return cv2.addWeighted(
            frame,
            0.6,
            overlay,
            0.4,
            0
        )
    
    @staticmethod
    def draw_timestamp(frame):
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cv2.putText(
            frame,
            timestamp,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        return frame

    # --------------------------------------------------------
    # Frame Number
    # --------------------------------------------------------

    @staticmethod
    def draw_frame_number(
        frame: np.ndarray,
        frame_number: int
    ) -> np.ndarray:
        """
        Draws the current frame number.
        """

        text = f"Frame: {frame_number}"

        (w, _), _ = cv2.getTextSize(
            text,
            cv2.FONT_HERSHEY_SIMPLEX,
            settings.DRAW_FONT_SCALE,
            settings.DRAW_BOX_THICKNESS
        )

        cv2.putText(
            frame,
            text,
            (
                frame.shape[1] - w - 20,
                frame.shape[0] - 20
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            settings.DRAW_FONT_SCALE,
            settings.DRAW_TEXT_COLOR,
            settings.DRAW_BOX_THICKNESS,
            cv2.LINE_AA
        )

        return frame
    
    # --------------------------------------------------------
    # Status Panel
    # --------------------------------------------------------

    @staticmethod
    def draw_status(
        frame,
        camera_name,
        fps,
        ai_status,
        gpu,
        weather=None
    ):
        """
        Draws the top-right status panel.
        """

        overlay = frame.copy()

        panel_width = 250
        panel_height = 135

        x1 = frame.shape[1] - panel_width - 20
        y1 = 50

        cv2.rectangle(
            overlay,
            (x1, y1),
            (x1 + panel_width, y1 + panel_height),
            (0,0,0),
            -1
        )

        frame = cv2.addWeighted(
            overlay,
            settings.DRAW_ALPHA,
            frame,
            1 - settings.DRAW_ALPHA,
            0
        )

        lines = [

            f"Camera : {camera_name}",

            f"FPS : {fps:.1f}",

            f"AI : {ai_status}",

            f"GPU : {gpu}",

            f"Weather : {weather or 'N/A'}"

        ]

        y = y1 + 25

        for line in lines:

            cv2.putText(

                frame,

                line,

                (x1 + 10, y),

                cv2.FONT_HERSHEY_SIMPLEX,

                settings.DRAW_FONT_SCALE,

                settings.DRAW_TEXT_COLOR,

                settings.DRAW_BOX_THICKNESS,

                cv2.LINE_AA

            )

            y += 22

        return frame
    
    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    @property
    def fps(self):

        if self.current_draw_time == 0:

            return 0

        return 1 / self.current_draw_time


    def info(self):

        avg = 0

        if self.frames_drawn:

            avg = self.total_draw_time / self.frames_drawn

        return {

            "frames_drawn": self.frames_drawn,

            "current_draw_time_ms":

                round(self.current_draw_time * 1000,2),

            "average_draw_time_ms":

                round(avg * 1000,2),

            "fps":

                round(

                    self.fps,

                    2

                )

        }
    
    # --------------------------------------------------------
    # Render Pipeline
    # --------------------------------------------------------

    @staticmethod
    def render(

        frame,

        detections=None,

        tracks=None,

        zones=None,

        statistics=None,

        alerts=None,

        fps=None,

        camera_name=None,

        frame_number=None,

        heatmap=None,

        status=None

    ):
        start = time.perf_counter()
        if heatmap is not None:

            frame = Drawing.draw_heatmap(
                frame,
                heatmap
            )

        if zones:

            for zone in zones:

                frame = Drawing.draw_zone(
                    frame,
                    **zone
                )

        if detections:

            frame = Drawing.draw_detections(
                frame,
                detections
            )

        if tracks:

            frame = Drawing.draw_tracks(
                frame,
                tracks
            )

        if statistics:

            frame = Drawing.draw_statistics(

                frame,

                people_count=statistics["people"]["people_count"],

                density=statistics["density"],

                occupancy=statistics["occupancy"]["occupancy_percentage"],

                temperature=statistics["weather"]["temperature"],

                # fps=statistics["fps"],

                risk_score=statistics["risk"]["risk_score"],

                # risk_level=statistics["risk_level"]

            )

        if alerts:

            if isinstance(alerts, list):

                for alert in alerts:

                    frame = Drawing.draw_alert(
                        frame,
                        **alert
                    )

            else:

                frame = Drawing.draw_alert(
                    frame,
                    **alerts
                )

        if camera_name:

            frame = Drawing.draw_camera_name(
                frame,
                camera_name
            )

        frame = Drawing.draw_timestamp(frame)

        if frame_number is not None:

            frame = Drawing.draw_frame_number(
                frame,
                frame_number
            )

        if fps is not None:

            frame = Drawing.draw_fps(
                frame,
                fps
            )

        if status:

            frame = Drawing.draw_status(

                frame,

                camera_name=status.get(
                    "camera",
                    camera_name
                ),

                fps=fps or 0,

                ai_status=status.get(
                    "ai",
                    "Running"
                ),

                gpu=status.get(
                    "gpu",
                    "CPU"
                ),

                weather=status.get(
                    "weather"
                )

            )

        Drawing.current_draw_time = (

            time.perf_counter() - start

        )

        Drawing.total_draw_time += (

            Drawing.current_draw_time

        )

        Drawing.frames_drawn += 1

        return frame