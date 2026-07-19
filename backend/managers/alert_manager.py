"""
============================================================
Astravon Live Arena
Alert Manager

Purpose:
    Centralized alert management for all cameras.

Responsibilities:
    • Store active alerts
    • Create alerts
    • Resolve alerts
    • Maintain alert history
    • Filter by severity
    • Dashboard summaries
    • Thread-safe

Author:
    House of Astravon

Version:
    2.0.0
============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from collections import deque
from typing import Dict, List, Optional
import uuid

from utils.logger import get_logger

logger = get_logger("AlertManager")


# ============================================================
# Alert Model
# ============================================================

@dataclass
class Alert:

    id: str

    camera_id: str

    title: str

    message: str

    severity: str

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    acknowledged: bool = False

    resolved: bool = False

    metadata: dict = field(default_factory=dict)


# ============================================================
# Alert Manager
# ============================================================

class AlertManager:

    def __init__(self):

        self._alerts: Dict[str, Alert] = {}

        self._history = deque(maxlen=1000)

        self._lock = Lock()

        logger.info("Alert Manager initialized.")

    # --------------------------------------------------------
    # Create Alert
    # --------------------------------------------------------

    def create(
        self,
        camera_id: str,
        title: str,
        message: str,
        severity: str = "medium",
        metadata: Optional[dict] = None
    ) -> Alert:

        alert = Alert(

            id=str(uuid.uuid4()),

            camera_id=camera_id,

            title=title,

            message=message,

            severity=severity.lower(),

            metadata=metadata or {}

        )

        with self._lock:

            self._alerts[alert.id] = alert

            self._history.appendleft(alert)

        logger.warning(
            f"[{camera_id}] {severity.upper()} -> {title}"
        )

        return alert

    # --------------------------------------------------------
    # Get Alert
    # --------------------------------------------------------

    def get(
        self,
        alert_id: str
    ) -> Optional[Alert]:

        return self._alerts.get(alert_id)

    # --------------------------------------------------------
    # Active Alerts
    # --------------------------------------------------------

    def active(
        self,
        camera_id: Optional[str] = None
    ) -> List[Alert]:

        alerts = [

            a for a in self._alerts.values()

            if not a.resolved

        ]

        if camera_id is not None:

            alerts = [

                a for a in alerts

                if a.camera_id == camera_id

            ]

        return sorted(

            alerts,

            key=lambda x: x.created_at,

            reverse=True

        )

    # --------------------------------------------------------
    # Alert History
    # --------------------------------------------------------

    def history(
        self,
        camera_id: Optional[str] = None
    ) -> List[Alert]:

        if camera_id is None:

            return list(self._history)

        return [

            a for a in self._history

            if a.camera_id == camera_id

        ]

    # --------------------------------------------------------
    # Acknowledge
    # --------------------------------------------------------

    def acknowledge(
        self,
        alert_id: str
    ) -> bool:

        alert = self._alerts.get(alert_id)

        if alert is None:

            return False

        with self._lock:

            alert.acknowledged = True

            alert.updated_at = datetime.utcnow()

        logger.info(
            f"Alert acknowledged: {alert.title}"
        )

        return True

    # --------------------------------------------------------
    # Resolve
    # --------------------------------------------------------

    def resolve(
        self,
        alert_id: str
    ) -> bool:

        alert = self._alerts.get(alert_id)

        if alert is None:

            return False

        with self._lock:

            alert.resolved = True

            alert.updated_at = datetime.utcnow()

        logger.info(
            f"Alert resolved: {alert.title}"
        )

        return True

    # --------------------------------------------------------
    # Remove
    # --------------------------------------------------------

    def remove(
        self,
        alert_id: str
    ):

        with self._lock:

            self._alerts.pop(alert_id, None)

    # --------------------------------------------------------
    # Clear
    # --------------------------------------------------------

    def clear_camera(
        self,
        camera_id: str
    ):

        with self._lock:

            ids = [

                aid

                for aid, alert in self._alerts.items()

                if alert.camera_id == camera_id

            ]

            for aid in ids:

                self._alerts.pop(aid, None)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    def summary(self):

        active = [

            a for a in self._alerts.values()

            if not a.resolved

        ]

        return {

            "total_active": len(active),

            "critical": len(

                [

                    a for a in active

                    if a.severity == "critical"

                ]

            ),

            "high": len(

                [

                    a for a in active

                    if a.severity == "high"

                ]

            ),

            "medium": len(

                [

                    a for a in active

                    if a.severity == "medium"

                ]

            ),

            "low": len(

                [

                    a for a in active

                    if a.severity == "low"

                ]

            )

        }

    # --------------------------------------------------------
    # Export
    # --------------------------------------------------------

    def snapshot(self):

        return [

            {

                "id": alert.id,

                "camera_id": alert.camera_id,

                "title": alert.title,

                "message": alert.message,

                "severity": alert.severity,

                "acknowledged": alert.acknowledged,

                "resolved": alert.resolved,

                "created_at": alert.created_at.isoformat(),

                "updated_at": alert.updated_at.isoformat(),

                "metadata": alert.metadata

            }

            for alert in self.active()

        ]

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(self):

        with self._lock:

            self._alerts.clear()

            self._history.clear()

        logger.info("Alert Manager reset.")

    # --------------------------------------------------------
    # Properties
    # --------------------------------------------------------

    @property
    def active_count(self):

        return len(

            [

                a

                for a in self._alerts.values()

                if not a.resolved

            ]

        )

    @property
    def history_count(self):

        return len(self._history)