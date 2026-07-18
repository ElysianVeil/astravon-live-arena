"""
============================================================
Astravon Live Arena
AI Engine Configuration

Purpose:
    Central configuration for the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from constants import COLOR_WHITE


# ============================================================
# Directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# ============================================================
# Settings
# ============================================================

class Settings(BaseSettings):
    """
    AI Engine configuration.
    """

    # --------------------------------------------------------
    # General
    # --------------------------------------------------------

    APP_NAME: str = "Astravon Live Arena AI Engine"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    LOG_LEVEL: str = "INFO"

    # --------------------------------------------------------
    # Backend Connection
    # --------------------------------------------------------

    BACKEND_URL: str = "http://127.0.0.1:8000"

    API_PREFIX: str = "/api/v1"

    WEBSOCKET_URL: str = "ws://127.0.0.1:8000/ws/engine"

    # --------------------------------------------------------
    # YOLO
    # --------------------------------------------------------

    YOLO_MODEL: Path = (
        BASE_DIR /
        "models" /
        "yolov_model" /
        "best.pt"
    )

    CONFIDENCE_THRESHOLD: float = 0.35

    IOU_THRESHOLD: float = 0.45

    DEVICE: str = "cpu"
    # Use "cuda" if NVIDIA GPU is available

    ENABLE_RESIZE: bool = True
    ENABLE_CLAHE: bool = True
    ENABLE_DENOISE: bool = True
    ENABLE_SHARPEN: bool = False
    ENABLE_GAMMA: bool = True
    ENABLE_AUTO_BRIGHTNESS: bool = True
    ENABLE_AUTO_DENOISE: bool = True
    ENABLE_NORMALIZE: bool = False
    DRAW_BOXES: bool = True
    DRAW_TRACKS: bool = True
    DRAW_LABELS: bool = True
    DRAW_FPS: bool = True
    DRAW_ALERTS: bool = True
    DRAW_STATISTICS: bool = True
    DRAW_ZONES: bool = True
    DRAW_HEATMAP: bool = False
    HEATMAP_MODE: str = "JET"
    DRAW_FONT_SCALE: float = 0.6
    DRAW_BOX_THICKNESS: int = 2
    DRAW_RADIUS: int = 8

    DRAW_ALPHA: float = 0.35

    DRAW_TEXT_COLOR: tuple = COLOR_WHITE

    DRAW_SHOW_CENTER: bool = True
    DRAW_SHOW_CONFIDENCE: bool = True
    DRAW_SHOW_TRAILS: bool = True
    DRAW_SHOW_HEATMAP: bool = True

    # --------------------------------------------------------
    # ByteTrack
    # --------------------------------------------------------

    TRACKER_ENABLED: bool = True

    TRACKER_CONFIDENCE: float = 0.50

    TRACK_BUFFER: int = 30

    MATCH_THRESHOLD: float = 0.80

    # --------------------------------------------------------
    # Camera
    # --------------------------------------------------------

    DEFAULT_CAMERA: int = 0

    FRAME_WIDTH: int = 1280

    FRAME_HEIGHT: int = 720

    FPS: int = 30

    MAX_CAMERAS: int = 8

    # --------------------------------------------------------
    # Detection
    # --------------------------------------------------------

    PERSON_CLASS_ID: int = 0

    DRAW_BOXES: bool = True

    DRAW_LABELS: bool = True

    DRAW_TRACKS: bool = True

    # --------------------------------------------------------
    # Crowd Analysis
    # --------------------------------------------------------

    LOW_DENSITY: int = 30

    MEDIUM_DENSITY: int = 80

    HIGH_DENSITY: int = 150

    # Total monitored area (square metres).
    VENUE_AREA: float = 1200.0

    VENUE_CAPACITY: int = 250

    MAX_OCCUPANCY: int = 500

    # ============================================================
    # Occupancy Thresholds
    # ============================================================

    OCCUPANCY_EMPTY: int = 25
    OCCUPANCY_MODERATE: int = 50
    OCCUPANCY_BUSY: int = 75
    OCCUPANCY_NEAR_FULL: int = 90
    OCCUPANCY_FULL: int = 100

    CONGESTION_OCCUPANCY_WEIGHT: float = 0.40

    CONGESTION_DENSITY_WEIGHT: float = 0.40

    CONGESTION_MOVEMENT_WEIGHT: float = 0.20

    # --------------------------------------------------------
    # Heat Simulation
    # --------------------------------------------------------

    DEFAULT_TEMPERATURE: float = 25.0

    DEFAULT_HUMIDITY: float = 55.0

    HEAT_WARNING: float = 35.0

    HEAT_DANGER: float = 40.0

    # --------------------------------------------------------
    # Risk Scoring
    # --------------------------------------------------------

    LOW_RISK: int = 30

    MEDIUM_RISK: int = 60

    HIGH_RISK: int = 80

    CRITICAL_RISK: int = 95

    # --------------------------------------------------------
    # Output Directories
    # --------------------------------------------------------

    OUTPUT_DIRECTORY: Path = (
        BASE_DIR / "outputs"
    )

    REPORT_DIRECTORY: Path = (
        BASE_DIR /
        "outputs" /
        "reports"
    )

    RECORDING_DIRECTORY: Path = (
        BASE_DIR /
        "outputs" /
        "recordings"
    )

    FRAME_DIRECTORY: Path = (
        BASE_DIR /
        "outputs" /
        "processed_frames"
    )

    LOG_DIRECTORY: Path = (
        BASE_DIR /
        "logs"
    )

    # --------------------------------------------------------
    # Assets
    # --------------------------------------------------------

    SAMPLE_VIDEO_DIRECTORY: Path = (
        BASE_DIR /
        "assets" /
        "sample_videos"
    )

    SAMPLE_IMAGE_DIRECTORY: Path = (
        BASE_DIR /
        "assets" /
        "sample_images"
    )

    DEMO_DIRECTORY: Path = (
        BASE_DIR /
        "assets" /
        "demo_data"
    )

    # --------------------------------------------------------
    # Pydantic Settings
    # --------------------------------------------------------

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# ============================================================
# Global Settings
# ============================================================

settings = Settings()


# ============================================================
# Create Required Directories
# ============================================================

settings.OUTPUT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

settings.REPORT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

settings.RECORDING_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

settings.FRAME_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

settings.LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Helper
# ============================================================

def print_configuration():
    """
    Prints the active AI Engine configuration.
    """

    print("=" * 60)
    print(settings.APP_NAME)
    print("=" * 60)
    print(f"Version        : {settings.APP_VERSION}")
    print(f"Debug          : {settings.DEBUG}")
    print(f"Device         : {settings.DEVICE}")
    print(f"YOLO Model     : {settings.YOLO_MODEL}")
    print(f"Backend URL    : {settings.BACKEND_URL}")
    print(f"Camera         : {settings.DEFAULT_CAMERA}")
    print(f"Resolution     : {settings.FRAME_WIDTH}x{settings.FRAME_HEIGHT}")
    print(f"FPS            : {settings.FPS}")
    print("=" * 60)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    print_configuration()