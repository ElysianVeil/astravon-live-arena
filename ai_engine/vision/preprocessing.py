"""
============================================================
Astravon Live Arena
Image Preprocessing

Purpose:
    Provides image preprocessing utilities before
    AI inference.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

from typing import Optional, Tuple

import cv2
import numpy as np

from config import settings
# from constants import (
#     DEFAULT_BLUR_KERNEL,
#     NORMALIZATION_DIVISOR,
# )
from utils.logger import get_logger
from utils.validators import validate_frame


# ============================================================
# Image Preprocessor
# ============================================================

logger = get_logger("Preprocessor")

class ImagePreprocessor:
    """
    Performs preprocessing operations on video frames.
    """

    def __init__(
        self,
        width: int = settings.FRAME_WIDTH,
        height: int = settings.FRAME_HEIGHT
    ) -> None:

        self.width = width
        self.height = height

    # ========================================================
    # Resize
    # ========================================================

    def resize(
        self,
        frame: np.ndarray,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> np.ndarray:
        """
        Resize a frame.
        """

        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame

        target_width = width or self.width
        target_height = height or self.height

        if target_width is None or target_height is None:
            return frame

        return cv2.resize(
            frame,
            (target_width, target_height)
        )

    # ========================================================
    # Gaussian Blur
    # ========================================================

    def blur(
        self,
        frame: np.ndarray,
        kernel_size: Tuple[int, int] = (5, 5)
    ) -> np.ndarray:
        """
        Applies Gaussian blur.
        """
        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame

        return cv2.GaussianBlur(
            frame,
            kernel_size,
            0
        )

    # ========================================================
    # Brightness
    # ========================================================

    def adjust_brightness(
        self,
        frame: np.ndarray,
        alpha: float = 1.0,
        beta: int = 0
    ) -> np.ndarray:
        """
        alpha -> contrast

        beta -> brightness
        """
        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame


        return cv2.convertScaleAbs(
            frame,
            alpha=alpha,
            beta=beta
        )

    # ========================================================
    # Histogram Equalization
    # ========================================================

    def equalize(
        self,
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Improves lighting.
        """

        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame

        ycrcb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2YCrCb
        )

        ycrcb[:, :, 0] = cv2.equalizeHist(
            ycrcb[:, :, 0]
        )

        return cv2.cvtColor(
            ycrcb,
            cv2.COLOR_YCrCb2BGR
        )

    # ========================================================
    # RGB Conversion
    # ========================================================

    def to_rgb(
        self,
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Converts BGR → RGB.
        """
        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame


        return cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

    # ========================================================
    # Grayscale
    # ========================================================

    def to_grayscale(
        self,
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Converts to grayscale.
        """
        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame

        return cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

    # ========================================================
    # Normalize
    # ========================================================

    def normalize(
        self,
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Normalize pixel values to 0–1.
        """
        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame

        return frame.astype(np.float32) / 255.0

    def denoise(
        self,
        frame: np.ndarray
    ) -> np.ndarray:

        return cv2.fastNlMeansDenoisingColored(
            frame,
            None,
            10,
            10,
            7,
            21
        )
    


    # ========================================================
    # Complete Pipeline
    # ========================================================

    def process(
        self,
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Standard preprocessing pipeline.

        This method can be modified later depending
        on lighting conditions.
        """
        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame

        image = frame.copy()

        image = self.resize(image)

        image = self.equalize(image)

        return image