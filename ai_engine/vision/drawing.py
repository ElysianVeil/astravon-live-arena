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
    COLOR_GRAY,
    COLOR_CYAN
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
    _cached_time = ""
    _last_second = -1

    # ============================================================
    # HUD Palette
    # ============================================================

    HUD_BACKGROUND = (24, 28, 36)
    HUD_PANEL = (34, 39, 49)
    HUD_BORDER = (65, 170, 255)

    HUD_TEXT = (240, 240, 240)
    HUD_SECONDARY = (185, 195, 205)

    SUCCESS = (70, 210, 110)
    WARNING = (0, 200, 255)
    DANGER = (60, 60, 255)
    INFO = (255, 200, 40)

    SHADOW = (0, 0, 0)

    # ============================================================
    # Layout
    # ============================================================

    PANEL_RADIUS = 12

    PANEL_MARGIN = 18

    PANEL_PADDING = 14

    HEADER_HEIGHT = 72

    FOOTER_HEIGHT = 82

    CARD_WIDTH = 170

    CARD_HEIGHT = 70

    CARD_SPACING = 12

    FONT = cv2.FONT_HERSHEY_SIMPLEX

    TITLE_SCALE = 0.75

    BODY_SCALE = 0.58

    SMALL_SCALE = 0.50

    @staticmethod
    def glass_overlay(
        frame: np.ndarray,
        alpha: float = 0.28
    ):

        overlay = frame.copy()

        return overlay, alpha
    
    
    # --------------------------------------------------------
    # Glass Panel
    # --------------------------------------------------------

    @staticmethod
    def draw_panel(
        overlay,
        x,
        y,
        w,
        h,
        border=True
    ):
        """
        Draws ONLY onto the overlay.
        No blending happens here.
        """

        cv2.rectangle(
            overlay,
            (x, y),
            (x + w, y + h),
            Drawing.HUD_PANEL,
            -1,
            cv2.LINE_AA
        )

        if border:

            cv2.rectangle(
                overlay,
                (x, y),
                (x + w, y + h),
                Drawing.HUD_BORDER,
                1,
                cv2.LINE_AA
            )

    
    
    @staticmethod
    def draw_text(
        frame,
        text,
        x,
        y,
        scale=None,
        color=None,
        thickness=1
    ):

        if scale is None:
            scale = Drawing.BODY_SCALE

        if color is None:
            color = Drawing.HUD_TEXT

        cv2.putText(
            frame,
            str(text),
            (int(x), int(y)),
            Drawing.FONT,
            scale,
            color,
            thickness,
            cv2.LINE_AA
        )

        return frame
    

    @staticmethod
    def draw_title(
        frame,
        title,
        x,
        y
    ):

        Drawing.draw_text(
            frame,
            title,
            x,
            y,
            Drawing.TITLE_SCALE,
            Drawing.HUD_BORDER,
            2
        )

        return frame
    
    @staticmethod
    def draw_key_value(
        frame,
        key,
        value,
        x,
        y
    ):

        Drawing.draw_text(
            frame,
            key,
            x,
            y,
            Drawing.SMALL_SCALE,
            Drawing.HUD_SECONDARY
        )

        Drawing.draw_text(
            frame,
            value,
            x + 90,
            y,
            Drawing.BODY_SCALE,
            Drawing.HUD_TEXT
        )

        return frame
    
    @staticmethod
    def draw_header(
        overlay,
        camera_name,
        fps
    ):

        h, w = overlay.shape[:2]

        margin = Drawing.PANEL_MARGIN

        height = Drawing.HEADER_HEIGHT

        Drawing.draw_panel(
           overlay,
            margin,
            margin,
            w - margin * 2,
            height
        )

        Drawing.draw_title(
            overlay,
            "ASTRAVON LIVE ARENA",
            margin + 18,
            margin + 28
        )

        Drawing.draw_text(
            overlay,
            camera_name,
            margin + 18,
            margin + 56
        )

        Drawing.draw_text(
            overlay,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            w - 250,
            margin + 28
        )

        Drawing.draw_text(
            overlay,
            f"{fps:.1f} FPS",
            w - 120,
            margin + 56,
            Drawing.TITLE_SCALE,
            Drawing.SUCCESS
        )

        Drawing.draw_text(
            overlay,
            f"{Drawing.live_detections} OBJECTS",
            w - 260,
            margin + 56,
            Drawing.BODY_SCALE,
            Drawing.INFO
        )

    
    @staticmethod
    def draw_card(
        overlay,
        x,
        y,
        title,
        value,
        color=None
    ):

        if color is None:
            color = Drawing.HUD_TEXT

        Drawing.draw_panel(
            overlay,
            x,
            y,
            Drawing.CARD_WIDTH,
            Drawing.CARD_HEIGHT
        )

        Drawing.draw_text(
            overlay,
            title,
            x + 12,
            y + 22,
            Drawing.SMALL_SCALE,
            Drawing.HUD_SECONDARY
        )

        Drawing.draw_text(
            overlay,
            value,
            x + 12,
            y + 52,
            Drawing.TITLE_SCALE,
            color,
            2
        )
    
    @staticmethod
    def draw_footer(
        overlay,
        statistics
    ):

        h, w = overlay.shape[:2]

        y = h - Drawing.FOOTER_HEIGHT - Drawing.PANEL_MARGIN

        x = Drawing.PANEL_MARGIN

        Drawing.draw_card(
            overlay,
            x,
            y,
            "People",
            str(statistics.get("people",{}).get("people_count",0))
        )

        x += Drawing.CARD_WIDTH + Drawing.CARD_SPACING

        Drawing.draw_card(
            overlay,
            x,
            y,
            "Occupancy",
            f'{statistics.get("occupancy",{}).get("occupancy_percentage",0.0):.1f}%'
        )

        x += Drawing.CARD_WIDTH + Drawing.CARD_SPACING

        Drawing.draw_card(
            overlay,
            x,
            y,
            "Temperature",
            f'{statistics.get("weather",{}).get("temperature",0.0):.1f}°C'
        )

        x += Drawing.CARD_WIDTH + Drawing.CARD_SPACING

        Drawing.draw_card(
            overlay,
            x,
            y,
            "Risk",
            str(statistics.get("risk",{}).get("risk_level","LOW")),
            Drawing.WARNING
        )

    

    # --------------------------------------------------------
    # Modern Detection Box
    # --------------------------------------------------------

    @staticmethod
    def draw_detection(
        frame: np.ndarray,
        bbox,
        label,
        confidence,
        color=None
    ):
        if color is None:

            if confidence > 0.90:
                color = COLOR_GREEN

            elif confidence > 0.75:
                color = COLOR_YELLOW

            elif confidence > 0.50:
                color = COLOR_ORANGE

            else:
                color = COLOR_RED

        x1,y1,x2,y2 = bbox

        Drawing.draw_corner_box(
            frame,
            x1,y1,x2,y2,
            color=color,
            thickness=2
        )

        text1 = label.upper()
        text2 = f"{confidence:.0%}"

        Drawing.draw_panel(
            frame,
            x1,
            y1 - 42,
            90,
            40,
            border=False
        )

        Drawing.draw_text(
            frame,
            text1,
            x1 + 8,
            y1 - 24,
            0.50
        )

        Drawing.draw_text(
            frame,
            text2,
            x1 + 8,
            y1 - 8,
            0.48,
            Drawing.SUCCESS
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
    # Corner Style Bounding Box
    # --------------------------------------------------------

    @staticmethod
    def draw_corner_box(
        frame,
        x1,
        y1,
        x2,
        y2,
        color,
        thickness=2,
        length=18
    ):

        # Top Left
        cv2.line(frame,(x1,y1),(x1+length,y1),color,thickness)
        cv2.line(frame,(x1,y1),(x1,y1+length),color,thickness)

        # Top Right
        cv2.line(frame,(x2,y1),(x2-length,y1),color,thickness)
        cv2.line(frame,(x2,y1),(x2,y1+length),color,thickness)

        # Bottom Left
        cv2.line(frame,(x1,y2),(x1+length,y2),color,thickness)
        cv2.line(frame,(x1,y2),(x1,y2-length),color,thickness)

        # Bottom Right
        cv2.line(frame,(x2,y2),(x2-length,y2),color,thickness)
        cv2.line(frame,(x2,y2),(x2,y2-length),color,thickness)

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
    def draw_track(frame,track):

        x1,y1,x2,y2 = track["bbox"]

        tid = track["track_id"]

        color=(255,200,60)

        Drawing.draw_corner_box(
            frame,
            x1,y1,x2,y2,
            color=color
        )

        cv2.circle(
            frame,
            ((x1+x2)//2,(y1+y2)//2),
            3,
            color,
            -1
        )

        Drawing.draw_text(
            frame,
            f"TRACK {tid}",
            x1,
            y1 - 8,
            scale=0.55,
            color=color,
            thickness=2
        )

        return frame
    
    # --------------------------------------------------------
    # Track Trail
    # --------------------------------------------------------

    @staticmethod
    def draw_trail(
        frame,
        points,
        color=(255,180,0)
    ):

        if len(points)<2:
            return frame

        for i in range(1,len(points)):

            alpha=i/len(points)

            thickness=max(1,int(alpha*4))

            cv2.line(
                frame,
                points[i-1],
                points[i],
                color,
                thickness,
                cv2.LINE_AA
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

    # @staticmethod
    # def draw_statistics(
    #     overlay,
    #     stats
    # ):

    #     x = 20
    #     y = 105

    #     width = 280
    #     height = 190

    #     Drawing.draw_panel(
    #         overlay,
    #         x,
    #         y,
    #         width,
    #         height
    #     )

    #     Drawing.draw_title(
    #         overlay,
    #         "AI SUMMARY",
    #         x + 15,
    #         y + 28
    #     )

    #     rows = [

    #         ("Persons",
    #         stats["people"]["people_count"]),

    #         ("Tracks",
    #         stats.get("tracking", {}).get("active_tracks", 0)),

    #         ("Vehicles",
    #         stats.get("vehicles", 0)),

    #         ("Density",
    #         stats["density"]["density_level"]),

    #         ("Risk",
    #         stats["risk"]["risk_level"]),

    #         ("Crowd Flow",
    #         stats.get("flow", "Unknown"))

    #     ]

    #     yy = y + 60

    #     for key, value in rows:

    #         Drawing.draw_key_value(
    #             overlay,
    #             key,
    #             value,
    #             x + 15,
    #             yy
    #         )

    #         yy += 24

    
    # --------------------------------------------------------
    # Weather Panel
    # --------------------------------------------------------

    @staticmethod
    def draw_weather_panel(
        overlay: np.ndarray,
        weather: Dict
    ):
        """
        Right-side environmental panel.

        Replaces:
            draw_weather()
        """

        width = 260
        height = 170

        x = overlay.shape[1] - width - 20
        y = 105

        Drawing.draw_panel(
            overlay,
            x,
            y,
            width,
            height
        )

        Drawing.draw_title(
            overlay,
            "WEATHER",
            x + 15,
            y + 28
        )

        rows = [

            (
                "Temperature",
                f'{weather.get("temperature",0):.1f} °C'
            ),

            (
                "Humidity",
                f'{weather.get("humidity",0):.0f}%'
            ),

            (
                "Wind",
                f'{weather.get("wind_speed",0):.1f} km/h'
            ),

            (
                "Condition",
                weather.get(
                    "condition",
                    "Unknown"
                )
            ),

            (
                "Feels Like",
                f'{weather.get("feels_like", weather.get("temperature",0)):.1f} °C'
            )

        ]

        yy = y + 58

        for key, value in rows:

            Drawing.draw_key_value(
                overlay,
                key,
                value,
                x + 15,
                yy
            )

            yy += 24


    # --------------------------------------------------------
    # Event Information Panel
    # --------------------------------------------------------

    @staticmethod
    def draw_event_panel(
        overlay: np.ndarray,
        event: Dict
    ):
        """
        Displays current event information.

        Expected dictionary:

        {
            "name": "...",
            "venue": "...",
            "attendance": 15230,
            "capacity": 20000,
            "phase": "LIVE"
        }
        """

        width = 320
        height = 180

        x = 20
        y = 370

        Drawing.draw_panel(
            overlay,
            x,
            y,
            width,
            height
        )

        Drawing.draw_title(
            overlay,
            "EVENT",
            x + 15,
            y + 28
        )

        attendance = event.get("attendance", 0)
        capacity = max(event.get("capacity", 1), 1)

        occupancy = attendance / capacity * 100

        rows = [

            (
                "Name",
                event.get("name", "Unknown")
            ),

            (
                "Venue",
                event.get("venue", "Unknown")
            ),

            (
                "Attendance",
                f"{attendance:,}"
            ),

            (
                "Capacity",
                f"{capacity:,}"
            ),

            (
                "Phase",
                event.get("phase", "LIVE")
            )

        ]

        yy = y + 58

        for key, value in rows:

            Drawing.draw_key_value(
                overlay,
                key,
                value,
                x + 15,
                yy
            )

            yy += 24

        # ----------------------------------------------------
        # Occupancy Bar
        # ----------------------------------------------------

        bar_x = x + 15
        bar_y = y + height - 24

        bar_w = width - 30
        bar_h = 12

        cv2.rectangle(
            overlay,
            (bar_x, bar_y),
            (bar_x + bar_w, bar_y + bar_h),
            (55, 55, 55),
            -1
        )

        fill = int(bar_w * min(occupancy, 100) / 100)

        if occupancy < 60:
            colour = Drawing.SUCCESS

        elif occupancy < 85:
            colour = Drawing.WARNING

        else:
            colour = Drawing.DANGER

        cv2.rectangle(
            overlay,
            (bar_x, bar_y),
            (bar_x + fill, bar_y + bar_h),
            colour,
            -1
        )

        Drawing.draw_text(
            overlay,
            f"{occupancy:.1f}% Occupancy",
            bar_x,
            bar_y - 6,
            Drawing.SMALL_SCALE,
            Drawing.HUD_SECONDARY
        )

    @staticmethod
    def draw_camera_health(
        overlay,
        health
    ):

        x = overlay.shape[1] - 270
        y = 245

        Drawing.draw_panel(
            overlay,
            x,
            y,
            250,
            130
        )

        Drawing.draw_title(
            overlay,
            "CAMERA",
            x + 15,
            y + 28
        )

        Drawing.draw_key_value(
            overlay,
            "Latency",
            f"{health['latency']} ms",
            x + 15,
            y + 55
        )

        Drawing.draw_key_value(
            overlay,
            "Bitrate",
            f"{health['bitrate']} Mbps",
            x + 15,
            y + 80
        )

        Drawing.draw_key_value(
            overlay,
            "Status",
            health["status"],
            x + 15,
            y + 105
        )

    @staticmethod
    def draw_ai_summary(
        overlay: np.ndarray,
        statistics: Dict
    ):
        """
        Left AI summary panel.

        Replaces:
            draw_statistics()
            draw_risk_indicator()
        """

        x = 20
        y = 105

        width = 300
        height = 245

        Drawing.draw_panel(
            overlay,
            x,
            y,
            width,
            height
        )

        Drawing.draw_title(
            overlay,
            "AI SUMMARY",
            x + 15,
            y + 28
        )

        people = statistics.get(
            "people",
            {}
        ).get(
            "people_count",
            0
        )

        tracks = statistics.get(
            "tracking",
            {}
        ).get(
            "active_tracks",
            0
        )

        vehicles = statistics.get(
            "vehicles",
            0
        )

        density = statistics.get(
            "density",
            {}
        ).get(
            "density_level",
            "LOW"
        )

        risk = statistics.get(
            "risk",
            {}
        ).get(
            "risk_level",
            "LOW"
        )

        flow = statistics.get(
            "flow",
            "UNKNOWN"
        )

        rows = [

            ("Persons", people),

            ("Tracks", tracks),

            ("Vehicles", vehicles),

            ("Density", density),

            ("Risk", risk),

            ("Flow", flow)

        ]

        yy = y + 60

        for key, value in rows:

            Drawing.draw_key_value(
                overlay,
                key,
                value,
                x + 15,
                yy
            )

            yy += 28

        # -----------------------
        # Risk Bar
        # -----------------------

        score = statistics.get(
            "risk",
            {}
        ).get(
            "risk_score",
            0
        )

        bar_x = x + 15
        bar_y = y + height - 32

        bar_w = width - 30
        bar_h = 14

        cv2.rectangle(
            overlay,
            (bar_x, bar_y),
            (bar_x + bar_w, bar_y + bar_h),
            (55, 55, 55),
            -1
        )

        fill = int(bar_w * (score / 100))

        if score < 40:
            colour = Drawing.SUCCESS

        elif score < 70:
            colour = Drawing.WARNING

        else:
            colour = Drawing.DANGER

        cv2.rectangle(
            overlay,
            (bar_x, bar_y),
            (bar_x + fill, bar_y + bar_h),
            colour,
            -1
        )

        Drawing.draw_text(
            overlay,
            f"Risk Score {score:.1f}/100",
            bar_x,
            bar_y - 8,
            Drawing.SMALL_SCALE,
            Drawing.HUD_SECONDARY
        )
    
    # # --------------------------------------------------------
    # # Risk Indicator
    # # --------------------------------------------------------

    # @staticmethod
    # def draw_risk_indicator(frame,score):

    #     x=20
    #     y=330

    #     width=240
    #     height=18

    #     cv2.rectangle(
    #         frame,
    #         (x,y),
    #         (x+width,y+height),
    #         (60,60,60),
    #         -1
    #     )

    #     score = max(0,min(score,100))
    #     fill = int(width*(score/100))

    #     if score<40:
    #         color=COLOR_GREEN

    #     elif score<70:
    #         color=COLOR_YELLOW

    #     elif score<90:
    #         color=COLOR_ORANGE

    #     else:
    #         color=COLOR_RED

    #     cv2.rectangle(
    #         frame,
    #         (x,y),
    #         (x+fill,y+height),
    #         color,
    #         -1
    #     )

    #     cv2.putText(
    #         frame,
    #         f"Risk {score:.1f}/100",
    #         (x,y-10),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         0.55,
    #         COLOR_WHITE,
    #         2,
    #         cv2.LINE_AA
    #     )

    #     return frame
    
    @staticmethod
    def draw_alert_stack(
        overlay,
        alerts
    ):

        x = overlay.shape[1] - 370
        y = 390

        for alert in alerts[:4]:

            Drawing.draw_alert(
                overlay,
                alert["title"],
                alert["severity"]
            )

            y += 55

    # --------------------------------------------------------
    # Alert
    # --------------------------------------------------------

    @staticmethod
    def draw_alert(overlay,title,severity):

        colors={

            "low":COLOR_GREEN,

            "medium":COLOR_YELLOW,

            "high":COLOR_ORANGE,

            "critical":COLOR_RED

        }

        color=colors.get(
            severity.lower(),
            COLOR_YELLOW
        )

        Drawing.draw_panel(
            overlay,
            380,
            20,
            520,
            50
        )

        cv2.circle(
            overlay,
            (400,45),
            8,
            color,
            -1
        )

        cv2.putText(
            overlay,
            title,
            (420,52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            COLOR_WHITE,
            2
        )


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
        overlay=cv2.GaussianBlur(
            overlay,
            (25,25),
            0
        )

        return cv2.addWeighted(
            frame,
            0.72,
            overlay,
            0.28,
            0
        )
    

    @staticmethod
    def get_timestamp():

        now = datetime.now()

        if now.second != Drawing._last_second:

            Drawing._cached_time = now.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            Drawing._last_second = now.second

        return Drawing._cached_time
    
    @staticmethod
    def draw_timestamp(frame):

        timestamp = Drawing.get_timestamp()

        Drawing.draw_text(
            frame,
            timestamp,
            25,
            frame.shape[0]-35,
            Drawing.SMALL_SCALE,
            Drawing.HUD_SECONDARY
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
    
    @staticmethod
    def draw_crowd_panel(
        overlay: np.ndarray,
        crowd: Dict
    ):
        """
        Crowd movement statistics.

        Expected dictionary

        {
            "average_speed": 1.25,
            "entering": 85,
            "exiting": 79,
            "standing": 142,
            "moving": 318,
            "direction": "North-East",
            "flow": "Stable"
        }
        """

        width = 320
        height = 210

        x = overlay.shape[1] - width - 20
        y = 390

        Drawing.draw_panel(
            overlay,
            x,
            y,
            width,
            height
        )

        Drawing.draw_title(
            overlay,
            "CROWD ANALYTICS",
            x + 15,
            y + 28
        )

        rows = [

            (
                "Avg Speed",
                f"{crowd.get('average_speed',0):.2f} m/s"
            ),

            (
                "Entering",
                crowd.get("entering",0)
            ),

            (
                "Exiting",
                crowd.get("exiting",0)
            ),

            (
                "Standing",
                crowd.get("standing",0)
            ),

            (
                "Moving",
                crowd.get("moving",0)
            ),

            (
                "Direction",
                crowd.get("direction","Unknown")
            )

        ]

        yy = y + 58

        for key,value in rows:

            Drawing.draw_key_value(
                overlay,
                key,
                value,
                x + 15,
                yy
            )

            yy += 24

        flow = crowd.get(
            "flow",
            "Stable"
        )

        colour = Drawing.SUCCESS

        if flow.lower() == "busy":
            colour = Drawing.WARNING

        elif flow.lower() == "congested":
            colour = Drawing.DANGER

        bar_x = x + 15
        bar_y = y + height - 24
        bar_w = width - 30
        bar_h = 12

        cv2.rectangle(
            overlay,
            (bar_x,bar_y),
            (bar_x+bar_w,bar_y+bar_h),
            (55,55,55),
            -1
        )

        if flow.lower() == "stable":
            fill = int(bar_w*0.35)

        elif flow.lower() == "busy":
            fill = int(bar_w*0.70)

        else:
            fill = bar_w

        cv2.rectangle(
            overlay,
            (bar_x,bar_y),
            (bar_x+fill,bar_y+bar_h),
            colour,
            -1
        )

        Drawing.draw_text(
            overlay,
            flow.upper(),
            bar_x,
            bar_y-8,
            Drawing.SMALL_SCALE,
            colour
        )
    
    # --------------------------------------------------------
    # Status Panel
    # --------------------------------------------------------

    # @staticmethod
    # def draw_status(
    #     overlay,
    #     camera_name,
    #     fps,
    #     ai_status,
    #     gpu,
    #     weather=None
    # ):
    #     """
    #     Draws the top-right status panel.
    #     """

    #     panel_width = 250
    #     panel_height = 135

    #     x1 = overlay.shape[1] - panel_width - 20
    #     y1 = 90

    #     Drawing.draw_panel(
    #         overlay,
    #         x1,
    #         y1,
    #         panel_width,
    #         panel_height
    #     )

    #     lines = [

    #         f"Camera : {camera_name}",
    #         f"FPS : {fps:.1f}",
    #         f"AI : {ai_status}",
    #         f"GPU : {gpu}",
    #         f"Weather : {weather or 'N/A'}"

    #     ]

    #     y = y1 + 28

    #     for line in lines:

    #         Drawing.draw_text(
    #             overlay,
    #             line,
    #             x1 + 12,
    #             y
    #         )

    #         y += 24

    #     return overlay
    
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
    # Modern Render Pipeline
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
        """
        Main rendering pipeline.

        Keeps the same API as previous versions while
        providing the new Astravon HUD.
        """

        start = time.perf_counter()

        overlay, alpha = Drawing.glass_overlay(frame)

        # ======================================================
        # Background Effects
        # ======================================================

        if heatmap is not None:
            frame = Drawing.draw_heatmap(frame, heatmap)

        if zones:
            for zone in zones:
                frame = Drawing.draw_zone(frame, **zone)

        # ======================================================
        # AI Detections
        # ======================================================

        if detections:
            Drawing.live_detections = len(detections or [])

            for det in detections:

                Drawing.draw_detection(
                    frame=frame,
                    bbox=det["bbox"],
                    label=det.get("class_name", "Object"),
                    confidence=det.get("confidence", 0.0)
                )

                Drawing.draw_center(
                    frame,
                    det["bbox"]
                )

        # ======================================================
        # Tracking
        # ======================================================

        if tracks:

            for track in tracks:

                Drawing.draw_track(
                    frame,
                    track
                )

                if "trail" in track:

                    Drawing.draw_trail(
                        frame,
                        track["trail"]
                    )

        # ======================================================
        # Statistics
        # ======================================================

        if statistics:

            try:

                Drawing.draw_ai_summary(
                    overlay,
                    statistics
                )

                # Optional modern weather card

                Drawing.draw_weather_panel(
                    overlay,
                    statistics.get("weather", {})
                )

            except Exception as e:

                logger.debug(
                    f"Statistics drawing skipped: {e}"
                )

        # ======================================================
        # Event Information
        # ======================================================

        event = None

        if statistics:
            event = statistics.get("event")

        if event:
            Drawing.draw_event_panel(
                overlay,
                event
            )

        if statistics:

            crowd = statistics.get("crowd")

            if crowd:

                Drawing.draw_crowd_panel(
                    overlay,
                    crowd
                )

        # ======================================================
        # Alerts
        # ======================================================

        if alerts:

            if isinstance(alerts, list):

                for alert in alerts:

                    Drawing.draw_alert(
                        overlay,
                        alert.get("title","Alert"),
                        alert.get("severity","medium")
                    )

            else:

                Drawing.draw_alert(
                    overlay,
                    **alerts
                )

            

        # ======================================================
        # Header
        # ======================================================

        if hasattr(Drawing, "draw_header"):

            Drawing.draw_header(
                overlay,
                camera_name or "Camera",
                fps or 0
            )

        else:

            Drawing.draw_camera_name(
                frame,
                camera_name or "Camera"
            )

        # ======================================================
        # Footer
        # ======================================================

        if hasattr(Drawing, "draw_footer"):

            if statistics is not None:

                Drawing.draw_footer(
                    overlay,
                    statistics
                )

        else:

            if fps is not None:

                Drawing.draw_fps(
                    frame,
                    fps
                )

            if frame_number is not None:

                Drawing.draw_frame_number(
                    frame,
                    frame_number
                )

        # ======================================================
        # Timestamp
        # ======================================================

        Drawing.draw_timestamp(frame)

        # ======================================================
        # Status Panel
        # ======================================================

        if status:

            Drawing.draw_status(

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

        # ======================================================
        # Rendering Metrics
        # ======================================================

        Drawing.current_draw_time = (
            time.perf_counter() - start
        )

        Drawing.total_draw_time += (
            Drawing.current_draw_time
        )

        Drawing.frames_drawn += 1

        cv2.addWeighted(
            overlay,
            alpha,
            frame,
            1-alpha,
            0,
            frame
        )

        return frame