"""
============================================================
Astravon Live Arena
AI Engine

Purpose:
    Entry point for the AI Engine.

Responsibilities:
    • Load configuration
    • Load YOLO model
    • Initialize camera manager
    • Start processing pipelines
    • Communicate with backend

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from pathlib import Path

from config import settings
from models.yolov_model.loader import YOLOModelLoader

from vision.camera_manager import CameraManager
from vision.pipeline import VisionPipeline

from utils.logger import get_logger
from analytics.metrics import MetricsManager


# ============================================================
# Logger
# ============================================================

logger = get_logger("AIEngine")


# ============================================================
# AI Engine
# ============================================================

class AIEngine:
    """
    Main AI Engine.

    Coordinates all computer vision modules.
    """

    def __init__(self):

        logger.info("Initializing AI Engine...")

        self.metrics = MetricsManager()

        # ----------------------------------------------------
        # Load Detection Model
        # ----------------------------------------------------

        self.model_loader = YOLOModelLoader(
            settings.YOLO_MODEL
        )

        self.model = self.model_loader.load()

        logger.info("YOLO model loaded successfully.")

        # ----------------------------------------------------
        # Camera Manager
        # ----------------------------------------------------

        self.camera_manager = CameraManager()

        # ----------------------------------------------------
        # Vision Pipeline
        # ----------------------------------------------------

        self.pipeline = VisionPipeline(
            camera_source=settings.DEFAULT_CAMERA,
            confidence=settings.CONFIDENCE_THRESHOLD,
            metrics=self.metrics,
            model=self.model,
            camera_manager=self.camera_manager
        )

    # ========================================================
    # Start Engine
    # ========================================================

    def start(self):
        """
        Starts the AI Engine.
        """

        logger.info("Starting AI Engine...")

        self.metrics.engine_status = "Running"

        self.pipeline.run()

    # ========================================================
    # Stop Engine
    # ========================================================

    def stop(self):
        """
        Stops the AI Engine.
        """

        logger.info("Stopping AI Engine...")

        self.metrics.engine_status = "Stopped"

        self.pipeline.stop()


# ============================================================
# Entry Point
# ============================================================

def main():
    """
    Starts the AI Engine.
    """

    logger.info("=" * 60)
    logger.info("Astravon Live Arena AI Engine")
    logger.info(f"Version : {settings.APP_VERSION}")
    logger.info("=" * 60)

    engine = AIEngine()

    try:

        engine.start()

    except KeyboardInterrupt:

        logger.info("Shutdown requested by user.")

        engine.metrics.engine_status = "Stopped"

    finally:

        engine.stop()

        logger.info("AI Engine stopped.")


# ============================================================
# Launch
# ============================================================

if __name__ == "__main__":
    main()