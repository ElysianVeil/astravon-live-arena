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
        self.frames_processed = 0

        self.processing_time = 0.0

        self.total_processing_time = 0.0

        self.last_operation = None

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
    # Resize (Keep Aspect Ratio)
    # ========================================================

    def resize_keep_ratio(
        self,
        frame: np.ndarray,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> np.ndarray:
        """
        Resize without stretching the image.
        Black padding is added where necessary.
        """

        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame

        target_width = width or self.width
        target_height = height or self.height

        h, w = frame.shape[:2]

        scale = min(
            target_width / w,
            target_height / h
        )

        new_width = int(w * scale)
        new_height = int(h * scale)

        resized = cv2.resize(
            frame,
            (new_width, new_height)
        )

        top = (target_height - new_height) // 2
        bottom = target_height - new_height - top

        left = (target_width - new_width) // 2
        right = target_width - new_width - left

        return cv2.copyMakeBorder(

            resized,

            top,

            bottom,

            left,

            right,

            cv2.BORDER_CONSTANT,

            value=(0, 0, 0)

        )
    
    # ========================================================
    # Letterbox Resize
    # ========================================================

    def letterbox(
        self,
        frame: np.ndarray,
        size: int = 640
    ) -> np.ndarray:
        """
        Performs YOLO-style letterbox resizing.
        """

        return self.resize_keep_ratio(
            frame,
            width=size,
            height=size
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
    # Automatic Noise Detection
    # ========================================================

    def smart_denoise(
        self,
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Only denoise noisy images.
        """

        if not validate_frame(frame):
            return frame

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        variance = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()

        if variance < 100:

            return self.denoise(frame)

        return frame
    
    def clahe(
        self,
        frame: np.ndarray
    ) -> np.ndarray:

        if not validate_frame(frame):
            return frame

        lab = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2LAB
        )

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8,8)
        )

        l = clahe.apply(l)

        merged = cv2.merge((l,a,b))

        return cv2.cvtColor(
            merged,
            cv2.COLOR_LAB2BGR
        )
    
    def gamma(
        self,
        frame,
        gamma=1.2
    ):

        inv = 1.0 / gamma

        table = np.array([

            ((i / 255.0) ** inv) * 255

            for i in np.arange(256)

        ]).astype("uint8")

        return cv2.LUT(frame, table)
    
    # ========================================================
    # Automatic Brightness
    # ========================================================

    def auto_brightness(
        self,
        frame: np.ndarray
    ) -> np.ndarray:
        """
        Automatically adjusts gamma
        depending on image brightness.
        """

        if not validate_frame(frame):
            return frame

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        mean = gray.mean()

        if mean < 70:

            return self.gamma(frame, 1.5)

        elif mean > 180:

            return self.gamma(frame, 0.8)

        return frame
    
    def sharpen(
        self,
        frame
    ):

        kernel = np.array([

            [0,-1,0],

            [-1,5,-1],

            [0,-1,0]

        ])

        return cv2.filter2D(
            frame,
            -1,
            kernel
        )
    
    def edge_enhance(
        self,
        frame
    ):

        edges = cv2.Canny(
            frame,
            100,
            200
        )

        return edges
    
    @property
    def average_processing_time(self):

        if self.frames_processed == 0:

            return 0

        return (

            self.total_processing_time

            /

            self.frames_processed

        )
    
    @property
    def max_processing_fps(self):

        if self.processing_time == 0:

            return 0

        return 1 / self.processing_time

    def info(self):

        return {

            "resolution": (

                self.width,

                self.height

            ),

            "frames_processed":

                self.frames_processed,

            "processing_time_ms":

                round(

                    self.processing_time*1000,

                    2

                ),

            "average_processing_time_ms":

                round(

                    self.average_processing_time*1000,

                    2

                ),

            "max_processing_fps":

                round(

                    self.max_processing_fps,

                    2

                )

        }

    # ========================================================
    # Complete Pipeline
    # ========================================================

    def process(
        self,
        frame: np.ndarray,
        profile="day"
    ) -> np.ndarray:
        """
        Standard preprocessing pipeline.

        This method can be modified later depending
        on lighting conditions.
        """
        if not validate_frame(frame):
            logger.warning("Invalid frame received.")
            return frame
        
        import time

        start = time.perf_counter()

        image = frame.copy()

        if profile == "day":

            if settings.ENABLE_RESIZE:

                image = self.resize(image)

        elif profile == "night":

            if settings.ENABLE_RESIZE:

                image = self.resize(image)

            if settings.ENABLE_CLAHE:

                image = self.clahe(image)

            if settings.ENABLE_AUTO_BRIGHTNESS:

                image = self.auto_brightness(image)

            if settings.ENABLE_DENOISE:

                image = self.smart_denoise(image)

        elif profile == "rain":

            if settings.ENABLE_RESIZE:

                image = self.resize(image)

            if settings.ENABLE_CLAHE:

                image = self.clahe(image)

            if settings.ENABLE_SHARPEN:

                image = self.sharpen(image)

            # if settings.ENABLE_NORMALIZATION:

            #     image = self.normalize(image)

        elapsed = time.perf_counter() - start

        self.processing_time = elapsed

        self.total_processing_time += elapsed

        self.frames_processed += 1

        return image