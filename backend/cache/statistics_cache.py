"""
============================================================
Astravon Live Arena
Statistics Cache

Purpose:
    Thread-safe in-memory cache for camera statistics.

Features
--------
- Latest statistics per camera
- Short rolling history
- Snapshot retrieval
- Automatic history trimming
- Dashboard ready
- Reporting ready

Author:
    House of Astravon
============================================================
"""

from __future__ import annotations

from collections import defaultdict, deque
from copy import deepcopy
from threading import Lock
from typing import Any, Dict, List, Optional


class StatisticsCache:
    """
    Stores live AI statistics.

    Structure

    latest
        camera_id -> newest statistics

    history
        camera_id -> deque(...)
    """

    def __init__(self, history_size: int = 300):

        self._latest: Dict[str, Dict[str, Any]] = {}

        self._history = defaultdict(
            lambda: deque(maxlen=history_size)
        )

        self._lock = Lock()

    # =====================================================
    # Latest
    # =====================================================

    def update(
        self,
        camera_id: str,
        statistics: Dict[str, Any]
    ) -> None:
        """
        Store newest statistics.
        """

        with self._lock:

            stats = deepcopy(statistics)

            self._latest[camera_id] = stats

            self._history[camera_id].append(stats)

    def get(
        self,
        camera_id: str
    ) -> Optional[Dict[str, Any]]:

        with self._lock:

            data = self._latest.get(camera_id)

            if data is None:
                return None

            return deepcopy(data)

    # =====================================================
    # History
    # =====================================================

    def history(
        self,
        camera_id: str
    ) -> List[Dict[str, Any]]:

        with self._lock:

            return deepcopy(
                list(
                    self._history[camera_id]
                )
            )

    def last(
        self,
        camera_id: str,
        count: int = 20
    ) -> List[Dict[str, Any]]:

        with self._lock:

            return deepcopy(
                list(self._history[camera_id])[-count:]
            )

    # =====================================================
    # Dashboard
    # =====================================================

    def all_latest(self):

        with self._lock:

            return deepcopy(self._latest)

    def cameras(self):

        with self._lock:

            return list(self._latest.keys())

    # =====================================================
    # Removal
    # =====================================================

    def remove_camera(
        self,
        camera_id: str
    ):

        with self._lock:

            self._latest.pop(camera_id, None)

            self._history.pop(camera_id, None)

    def clear(self):

        with self._lock:

            self._latest.clear()

            self._history.clear()

    # =====================================================
    # Counts
    # =====================================================

    @property
    def camera_count(self):

        return len(self._latest)

    def history_size(
        self,
        camera_id: str
    ):

        return len(
            self._history[camera_id]
        )


statistics_cache = StatisticsCache()