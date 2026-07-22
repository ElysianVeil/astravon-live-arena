"""
============================================================
Astravon Live Arena
Identity Database

Purpose:
    Stores and manages global identities for
    multi-camera person re-identification (ReID).

Responsibilities
----------------
• Assign Global IDs
• Store embeddings
• Match identities
• Update identities
• Remove stale identities
• Maintain statistics

Author:
    House of Astravon

Version:
    2.0.0
============================================================
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np

from config import settings
from utils.logger import get_logger


# ============================================================
# Logger
# ============================================================

logger = get_logger("IdentityDatabase")


# ============================================================
# Identity Record
# ============================================================

@dataclass
class IdentityRecord:
    """
    Represents one globally tracked person.
    """

    global_id: int

    embedding: np.ndarray

    first_seen: datetime

    last_seen: datetime

    camera_id: str

    bbox: Optional[List] = None

    appearances: int = 1

    confidence: float = 1.0

    metadata: Dict = field(default_factory=dict)


# ============================================================
# Identity Database
# ============================================================

class IdentityDatabase:
    """
    Global identity manager.

    Shared by every camera.
    """

    def __init__(self):

        logger.info("Initializing Identity Database...")

        self.lock = threading.RLock()

        self.identities: Dict[int, IdentityRecord] = {}

        self.next_global_id = 1

        self.similarity_threshold = getattr(
            settings,
            "REID_SIMILARITY_THRESHOLD",
            0.75
        )

        self.maximum_identity_age = getattr(
            settings,
            "REID_MAX_AGE_SECONDS",
            600
        )

        self.maximum_database_size = getattr(
            settings,
            "REID_DATABASE_SIZE",
            10000
        )

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        self.total_registered = 0

        self.total_matches = 0

        self.total_new_people = 0

        self.total_updates = 0

        self.total_removed = 0

        self.total_queries = 0

        self.maximum_population = 0

        self.last_registered = None

        self.last_match = None

        logger.info("Identity Database initialized.")

        # ========================================================
    # Register Identity
    # ========================================================

    def register(
        self,
        embedding: np.ndarray,
        camera_id: str,
        confidence: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> int:

        with self.lock:

            global_id = self.next_global_id

            self.next_global_id += 1

            now = datetime.utcnow()

            self.identities[global_id] = IdentityRecord(
                global_id=global_id,
                embedding=embedding.copy(),
                first_seen=now,
                last_seen=now,
                camera_id=camera_id,
                confidence=confidence,
                metadata=metadata or {}
            )

            self.total_registered += 1
            self.total_new_people += 1

            self.maximum_population = max(
                self.maximum_population,
                len(self.identities)
            )

            self.last_registered = global_id

            logger.debug(
                f"Registered Global ID {global_id}"
            )

            return global_id

    # ========================================================
    # Match Identity
    # ========================================================

    def match(
        self,
        embedding: np.ndarray
    ) -> Optional[int]:

        with self.lock:

            self.total_queries += 1

            if not self.identities:
                return None

            best_similarity = -1.0
            best_id = None

            for global_id, record in self.identities.items():

                similarity = float(
                    np.dot(embedding, record.embedding) /
                    (
                        np.linalg.norm(embedding) *
                        np.linalg.norm(record.embedding) +
                        1e-12
                    )
                )

                if similarity > best_similarity:

                    best_similarity = similarity
                    best_id = global_id

            if (
                best_id is not None
                and
                best_similarity >= self.similarity_threshold
            ):

                self.total_matches += 1
                self.last_match = best_id

                return best_id

            return None

    # ========================================================
    # Update Identity
    # ========================================================

    def update(
        self,
        global_id: int,
        embedding: np.ndarray,
        camera_id: str,
        bbox=None
    ) -> bool:

        with self.lock:

            if global_id not in self.identities:
                return False

            identity = self.identities[global_id]

            alpha = 0.2

            identity.embedding = (
                (1 - alpha) * identity.embedding
                +
                alpha * embedding
            )

            identity.embedding /= (
                np.linalg.norm(identity.embedding)
                + 1e-12
            )

            identity.last_seen = datetime.utcnow()

            identity.camera_id = camera_id

            identity.bbox = (
                [int(v) for v in bbox]
                if bbox is not None
                else None
            )

            identity.appearances += 1

            self.total_updates += 1

            return True

    # ========================================================
    # Resolve Identity
    # ========================================================

    def resolve(
        self,
        embedding: np.ndarray,
        camera_id: str
    ) -> int:

        global_id = self.match(embedding)

        if global_id is None:

            return self.register(
                embedding,
                camera_id
            )

        self.update(
            global_id,
            embedding,
            camera_id
        )

        return global_id

    # ========================================================
    # Cleanup
    # ========================================================

    def cleanup(self):

        with self.lock:

            now = datetime.utcnow()

            expired = []

            for global_id, record in self.identities.items():

                age = (
                    now -
                    record.last_seen
                ).total_seconds()

                if age > self.maximum_identity_age:

                    expired.append(global_id)

            for global_id in expired:

                del self.identities[global_id]

                self.total_removed += 1

            if expired:

                logger.info(
                    f"Removed {len(expired)} expired identities."
                )

    # ========================================================
    # Get Identity
    # ========================================================

    def get(
        self,
        global_id: int
    ) -> Optional[IdentityRecord]:

        return self.identities.get(global_id)

    # ========================================================
    # Current Population
    # ========================================================

    def population(self) -> int:

        return len(self.identities)

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(self) -> Dict:

        average_appearances = 0.0

        if self.identities:

            average_appearances = sum(

                identity.appearances

                for identity in self.identities.values()

            ) / len(self.identities)

        return {

            "current_population": len(self.identities),

            "maximum_population": self.maximum_population,

            "registered": self.total_registered,

            "matches": self.total_matches,

            "new_people": self.total_new_people,

            "updates": self.total_updates,

            "removed": self.total_removed,

            "queries": self.total_queries,

            "average_appearances": round(
                average_appearances,
                2
            )
        }

    # ========================================================
    # Dashboard
    # ========================================================

    def summary(self) -> Dict:

        return {

            "active_people": len(self.identities),

            "registered": self.total_registered,

            "matches": self.total_matches,

            "queries": self.total_queries,

            "removed": self.total_removed
        }

    # ========================================================
    # Module Information
    # ========================================================

    def info(self) -> Dict:

        with self.lock:

            identities = []

            for identity in self.identities.values():

                identities.append({

                    "global_id": identity.global_id,

                    "camera_id": identity.camera_id,

                    "appearances": identity.appearances,

                    "confidence": round(identity.confidence, 3),

                    "first_seen": identity.first_seen.isoformat(),

                    "last_seen": identity.last_seen.isoformat(),

                    "bbox": identity.bbox

                })

            return {

                "module": "Identity Database",

                "status": "Running",

                "population": len(self.identities),

                "similarity_threshold": self.similarity_threshold,

                "maximum_identity_age": self.maximum_identity_age,

                "database_size_limit": self.maximum_database_size,

                "statistics": self.statistics(),

                "identities": identities

            }
    
    def all_identities(self):
        with self.lock:
            return list(self.identities.values())

    # ========================================================
    # Reset
    # ========================================================

    def reset(self):

        with self.lock:

            self.identities.clear()

            self.next_global_id = 1

            self.total_registered = 0
            self.total_matches = 0
            self.total_new_people = 0
            self.total_updates = 0
            self.total_removed = 0
            self.total_queries = 0

            self.maximum_population = 0

            self.last_registered = None
            self.last_match = None

            logger.warning(
                "Identity Database reset."
            )


# ============================================================
# Singleton
# ============================================================

identity_database = IdentityDatabase()