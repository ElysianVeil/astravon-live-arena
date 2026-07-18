"""
============================================================
Astravon Live Arena
Feature Extractor

Purpose:
    Extracts appearance embeddings from detected people
    for Multi-Camera Person Re-Identification (ReID).

    This module converts a cropped person image into a
    normalized feature vector that uniquely represents
    the person's appearance.

    The embeddings are later used by the Identity Matcher
    to assign a global person ID across multiple cameras.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import time
from collections import deque
from pathlib import Path
from typing import List, Optional, Dict, Any

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from numpy.typing import NDArray
from PIL import Image
from torchvision import transforms

import torch.nn as nn
from reid.models.osnet import osnet_x1_0

from config import settings
from utils.logger import get_logger


# ============================================================
# Logger
# ============================================================

logger = get_logger("FeatureExtractor")


# ============================================================
# Feature Extractor
# ============================================================

class ReIDFeatureExtractor:
    """
    Production-grade Person Re-Identification Feature Extractor.

    Responsibilities
    ----------------
    • Load pretrained ReID model
    • Extract person embeddings
    • Normalize embeddings
    • Batch feature extraction
    • Measure inference performance
    • Maintain runtime statistics
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self):

        logger.info("Initializing ReID Feature Extractor...")

        # ----------------------------------------------------
        # Runtime
        # ----------------------------------------------------

        self.running = False

        self.model_loaded = False

        self.model_name = "osnet_x1_0"

        self.embedding_size = 512

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        logger.info(
            f"Using device: {self.device.upper()}"
        )

        # ----------------------------------------------------
        # Model Location
        # ----------------------------------------------------

        self.model_directory = (
            Path(__file__).parent /
            "models"
        )

        self.model_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.model_path = (
            self.model_directory /
            "osnet_x1_0_imagenet.pth"
        )

        # ----------------------------------------------------
        # Image Parameters
        # ----------------------------------------------------

        self.image_width = 128

        self.image_height = 256

        self.batch_size = 32

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        self.total_extractions = 0

        self.failed_extractions = 0

        self.total_batches = 0

        self.total_processing_time = 0.0

        self.average_time = 0.0

        self.maximum_time = 0.0

        self.minimum_time = float("inf")

        self.last_extraction = None

        self.last_embedding = None

        self.history = deque(maxlen=500)

        # ----------------------------------------------------
        # Image Preprocessing
        # ----------------------------------------------------

        self.transform = transforms.Compose([

            transforms.Resize(
                (
                    self.image_height,
                    self.image_width
                )
            ),

            transforms.ToTensor(),

            transforms.Normalize(

                mean=[
                    0.485,
                    0.456,
                    0.406
                ],

                std=[
                    0.229,
                    0.224,
                    0.225
                ]

            )

        ])

        # ----------------------------------------------------
        # Load AI Model
        # ----------------------------------------------------

        self.model = None

        self.load_model()

        if self.model_loaded:

            self.warmup()

            self.running = True

            logger.info(
                "ReID Feature Extractor ready."
            )

    # ========================================================
    # Load Model
    # ========================================================

    def load_model(self) -> bool:
        """
        Loads the pretrained OSNet model.
        """

        try:

            logger.info(
                "Loading OSNet ReID model..."
            )

            self.model = osnet_x1_0(
                pretrained=False,
                num_classes=1000
            )

            state = torch.load(
                self.model_path,
                map_location=self.device
            )

            self.model.load_state_dict(state)

            self.model.eval()

            self.model.to(self.device)

            self.model_loaded = True

            logger.info(
                "OSNet model loaded successfully."
            )

            return True

        except Exception as error:

            logger.exception(error)

            self.model_loaded = False

            return False

    # ========================================================
    # Warmup
    # ========================================================

    def warmup(self):
        """
        Runs a dummy inference so the first
        real prediction is fast.
        """

        if not self.model_loaded:

            return

        logger.info(
            "Running model warmup..."
        )

        dummy = np.zeros(

            (
                self.image_height,
                self.image_width,
                3
            ),

            dtype=np.uint8

        )

        try:

            dummy = torch.zeros(
                1,
                3,
                256,
                128
            ).to(self.device)

            with torch.no_grad():

                self.model(dummy)

            logger.info(
                "Warmup complete."
            )

        except Exception as error:

            logger.warning(
                f"Warmup failed: {error}"
            )

        # ========================================================
    # Extract Features
    # ========================================================

    def extract(
        self,
        person_crop: NDArray[np.uint8]
    ) -> Optional[NDArray[np.float32]]:
        """
        Extracts a normalized feature embedding
        from a cropped person image.

        Returns
        -------
        np.ndarray | None
        """

        if not self.model_loaded:

            logger.error(
                "Feature extractor model is not loaded."
            )

            return None

        if person_crop is None:

            self.failed_extractions += 1

            return None

        if person_crop.size == 0:

            self.failed_extractions += 1

            return None

        start = time.perf_counter()

        try:

            rgb = cv2.cvtColor(
                person_crop,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(rgb)

            tensor = self.transform(image)

            tensor = tensor.unsqueeze(0)

            tensor = tensor.to(self.device)

            with torch.no_grad():

                embedding = self.model(tensor)

            embedding = embedding.squeeze(0)

            embedding = embedding.cpu().numpy()

            embedding = self.normalize(
                embedding
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            self.total_extractions += 1

            self.total_processing_time += elapsed / 1000.0

            self.last_embedding = embedding

            self.last_extraction = time.time()

            self.maximum_time = max(

                self.maximum_time,

                elapsed

            )

            self.minimum_time = min(

                self.minimum_time,

                elapsed

            )

            self.average_time = (

                (

                    self.average_time

                    *

                    (

                        self.total_extractions - 1

                    )

                )

                +

                elapsed

            ) / self.total_extractions

            self.history.append(

                {

                    "timestamp": self.last_extraction,

                    "time_ms": round(

                        elapsed,

                        2

                    ),

                    "success": True

                }

            )

            return embedding.astype(

                np.float32

            )

        except Exception as error:

            logger.exception(error)

            self.failed_extractions += 1

            self.history.append(

                {

                    "timestamp": time.time(),

                    "time_ms": 0,

                    "success": False

                }

            )

            return None

    # ========================================================
    # Batch Extraction
    # ========================================================

    def batch_extract(
        self,
        person_crops: List[NDArray[np.uint8]]
    ) -> List[NDArray[np.float32]]:
        """
        Extracts embeddings for multiple people.

        Parameters
        ----------
        person_crops

            List of OpenCV images.

        Returns
        -------
        list[np.ndarray]
        """

        embeddings = []

        self.total_batches += 1

        images = []

        for crop in person_crops:

            rgb = cv2.cvtColor(
                crop,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(rgb)

            images.append(
                self.transform(image)
            )

        start = time.perf_counter()

        batch = torch.stack(images).to(self.device)

        with torch.no_grad():
            embeddings = self.model(batch)

        elapsed = time.perf_counter() - start

        self.total_processing_time += elapsed
        self.total_batches += 1

        embeddings = embeddings.cpu().numpy()

        return embeddings

    # ========================================================
    # Normalize
    # ========================================================

    def normalize(
        self,
        embedding: NDArray
    ) -> NDArray:
        """
        Performs L2 normalization.
        """

        norm = np.linalg.norm(
            embedding
        )

        if norm == 0:

            return embedding

        return embedding / norm

    # ========================================================
    # Cosine Similarity
    # ========================================================

    def cosine_similarity(
        self,
        embedding_a: NDArray,
        embedding_b: NDArray
    ) -> float:
        """
        Computes cosine similarity.

        Returns
        -------
        float

        Range

            -1.0

                to

            1.0
        """

        embedding_a = self.normalize(
            embedding_a
        )

        embedding_b = self.normalize(
            embedding_b
        )

        similarity = np.dot(

            embedding_a,

            embedding_b

        )

        return float(similarity)

    # ========================================================
    # Euclidean Distance
    # ========================================================

    def euclidean_distance(
        self,
        embedding_a: NDArray,
        embedding_b: NDArray
    ) -> float:
        """
        Computes Euclidean distance.

        Lower values indicate
        greater similarity.
        """

        return float(

            np.linalg.norm(

                embedding_a -

                embedding_b

            )

        )

    # ========================================================
    # Compare
    # ========================================================

    def compare(
        self,
        embedding_a: NDArray,
        embedding_b: NDArray,
        threshold: float = 0.85
    ) -> bool:
        """
        Determines whether two embeddings
        belong to the same person.
        """

        similarity = self.cosine_similarity(

            embedding_a,

            embedding_b

        )

        return similarity >= threshold

    # ========================================================
    # Embedding Quality
    # ========================================================

    def embedding_quality(
        self,
        embedding: NDArray
    ) -> dict:
        """
        Returns simple diagnostics for
        an embedding.
        """

        return {

            "dimensions": int(

                embedding.shape[0]

            ),

            "norm": round(

                float(

                    np.linalg.norm(

                        embedding

                    )

                ),

                4

            ),

            "minimum": round(

                float(

                    np.min(

                        embedding

                    )

                ),

                4

            ),

            "maximum": round(

                float(

                    np.max(

                        embedding

                    )

                ),

                4

            ),

            "mean": round(

                float(

                    np.mean(

                        embedding

                    )

                ),

                4

            )

        }
    
    # ============================================================
    # Statistics
    # ============================================================

    def statistics(self) -> Dict[str, Any]:
        """
        Returns feature extraction statistics.
        """

        average_time = (
            self.total_processing_time / self.total_extractions
            if self.total_extractions
            else 0.0
        )

        return {
            "total_extractions": self.total_extractions,
            "failed_extractions": self.failed_extractions,
            "average_processing_time_ms": round(
                average_time * 1000,
                2
            ),
            "device": self.device,
            "embedding_dimension": self.embedding_size,
            "model_loaded": self.model is not None,
            "model_name": self.model_name
        }


    # ============================================================
    # Last Embedding
    # ============================================================

    def last_embedding(self) -> Optional[np.ndarray]:
        """
        Returns the last extracted embedding.
        """

        return self._last_embedding


    # ============================================================
    # Processing Time
    # ============================================================

    def average_processing_time(self) -> float:
        """
        Average extraction time in milliseconds.
        """

        if self.total_extractions == 0:
            return 0.0

        return round(
            (
                self.total_processing_time
                / self.total_extractions
            )
            * 1000,
            2
        )


    # ============================================================
    # GPU Information
    # ============================================================

    def gpu_information(self) -> Dict[str, Any]:
        """
        Returns GPU information.
        """

        if not torch.cuda.is_available():

            return {
                "available": False
            }

        return {
            "available": True,
            "device": torch.cuda.get_device_name(0),
            "memory_allocated_mb": round(
                torch.cuda.memory_allocated() / 1024 ** 2,
                2
            ),
            "memory_reserved_mb": round(
                torch.cuda.memory_reserved() / 1024 ** 2,
                2
            )
        }


    # ============================================================
    # Health Check
    # ============================================================

    def health(self) -> Dict[str, Any]:
        """
        Returns extractor health.
        """

        return {
            "status": (
                "Running"
                if self.model is not None
                else "Unavailable"
            ),
            "device": self.device.type,
            "model_loaded": self.model is not None,
            "ready": self.model is not None
        }


    # ============================================================
    # Summary
    # ============================================================

    def summary(self) -> Dict[str, Any]:
        """
        Returns a lightweight dashboard summary.
        """

        return {
            "status": (
                "Running"
                if self.model is not None
                else "Stopped"
            ),
            "device": self.device.type,
            "model": self.model_name,
            "embeddings": self.total_extractions,
            "average_time_ms": self.average_processing_time()
        }


    # ============================================================
    # Module Information
    # ============================================================

    def info(self) -> Dict[str, Any]:
        """
        Returns module information.
        """

        return {
            "module": "Feature Extractor",
            "version": "1.0.0",
            "status": (
                "Running"
                if self.model is not None
                else "Stopped"
            ),
            "device": self.device,
            "model": self.model_name,
            "embedding_dimension": self.embedding_size,
            "statistics": self.statistics()
        }


    # ============================================================
    # Clear Cache
    # ============================================================

    def clear_cache(self) -> None:
        """
        Clears cached tensors.
        """

        self._last_embedding = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()


    # ============================================================
    # Reset Statistics
    # ============================================================

    def reset(self) -> None:
        """
        Resets runtime statistics.
        """

        self.total_extractions = 0
        self.failed_extractions = 0
        self.total_processing_time = 0.0

        self._last_embedding = None


    # ============================================================
    # Warmup
    # ============================================================

    # def warmup(self) -> None:
    #     """
    #     Performs a dummy inference to reduce
    #     first-frame latency.
    #     """

    #     dummy = np.zeros(
    #         (256, 128, 3),
    #         dtype=np.uint8
    #     )

    #     try:
    #         self.extract(dummy)
    #     except Exception:
    #         pass


    # ============================================================
    # Shutdown
    # ============================================================

    def shutdown(self) -> None:
        """
        Releases GPU memory.
        """

        self.clear_cache()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()


# ============================================================
# Singleton
# ============================================================

feature_extractor = ReIDFeatureExtractor()