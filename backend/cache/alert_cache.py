"""
============================================================
Astravon Live Arena
Alert Cache

Purpose:
    Thread-safe in-memory cache for AI alerts.

Features
--------
- Stores active alerts
- Alert history
- Per-camera alerts
- Alert acknowledgement
- Automatic expiration support
- Dashboard ready

Author:
    House of Astravon
============================================================
"""

from __future__ import annotations

from collections import defaultdict, deque
from copy import deepcopy
from datetime import datetime
from threading import Lock
from typing import Any, Dict, List, Optional
import uuid


class AlertCache:
    """
    Stores AI-generated alerts.

    Structure
    ---------

    active
        camera_id -> {alert_id: alert}

    history
        camera_id -> deque(alert)
    """

    def __init__(self, history_size: int = 500):

        self._active: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)

        self._history = defaultdict(
            lambda: deque(maxlen=history_size)
        )

        self._lock = Lock()

    # =====================================================
    # Alert Creation
    # =====================================================

    def create(
        self,
        camera_id: str,
        title: str,
        severity: str,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Creates a new alert.

        Returns
        -------
        alert_id
        """

        with self._lock:

            alert_id = str(uuid.uuid4())

            alert = {
                "id": alert_id,
                "camera_id": camera_id,
                "title": title,
                "severity": severity.lower(),
                "description": description,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat(),
                "acknowledged": False,
                "resolved": False
            }

            self._active[camera_id][alert_id] = alert

            self._history[camera_id].append(
                deepcopy(alert)
            )

            return alert_id

    # =====================================================
    # Retrieval
    # =====================================================

    def get(
        self,
        camera_id: str,
        alert_id: str
    ) -> Optional[Dict[str, Any]]:

        with self._lock:

            alert = self._active[camera_id].get(alert_id)

            if alert is None:
                return None

            return deepcopy(alert)

    def active(
        self,
        camera_id: str
    ) -> List[Dict[str, Any]]:

        with self._lock:

            return deepcopy(
                list(
                    self._active[camera_id].values()
                )
            )

    def active_all(self) -> Dict[str, List[Dict[str, Any]]]:

        with self._lock:

            return {
                camera: deepcopy(list(alerts.values()))
                for camera, alerts in self._active.items()
            }

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

    # =====================================================
    # State Changes
    # =====================================================

    def acknowledge(
        self,
        camera_id: str,
        alert_id: str
    ) -> bool:

        with self._lock:

            alert = self._active[camera_id].get(alert_id)

            if alert is None:
                return False

            alert["acknowledged"] = True

            return True

    def resolve(
        self,
        camera_id: str,
        alert_id: str
    ) -> bool:

        with self._lock:

            alert = self._active[camera_id].pop(
                alert_id,
                None
            )

            if alert is None:
                return False

            alert["resolved"] = True

            self._history[camera_id].append(
                deepcopy(alert)
            )

            return True

    # =====================================================
    # Removal
    # =====================================================

    def clear_camera(
        self,
        camera_id: str
    ):

        with self._lock:

            self._active.pop(camera_id, None)

            self._history.pop(camera_id, None)

    def clear(self):

        with self._lock:

            self._active.clear()

            self._history.clear()

    # =====================================================
    # Metrics
    # =====================================================

    def active_count(
        self,
        camera_id: Optional[str] = None
    ) -> int:

        with self._lock:

            if camera_id is not None:

                return len(
                    self._active[camera_id]
                )

            return sum(
                len(alerts)
                for alerts in self._active.values()
            )

    def cameras(self):

        with self._lock:

            return list(self._active.keys())

    # =====================================================
    # Severity Filtering
    # =====================================================

    def by_severity(
        self,
        severity: str
    ) -> List[Dict[str, Any]]:

        severity = severity.lower()

        alerts = []

        with self._lock:

            for camera_alerts in self._active.values():

                for alert in camera_alerts.values():

                    if alert["severity"] == severity:

                        alerts.append(
                            deepcopy(alert)
                        )

        return alerts


# ============================================================
# Singleton
# ============================================================

alert_cache = AlertCache()