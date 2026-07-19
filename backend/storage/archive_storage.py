"""
============================================================
Astravon Live Arena
Archive Storage

Purpose:
    Persists completed events and archived statistics
    into JSON files for historical analysis.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from threading import Lock
from typing import Any, Dict, List

from utils.logger import get_logger

logger = get_logger("ArchiveStorage")


class ArchiveStorage:
    """
    Handles long-term archive storage.

    Structure

    storage/
        archive/
            events/
                2026-07-18.json
            statistics/
                2026-07-18.json
            alerts/
                2026-07-18.json
    """

    def __init__(
        self,
        root: str = "storage/archive"
    ):

        self.root = Path(root)

        self.events_dir = self.root / "events"
        self.statistics_dir = self.root / "statistics"
        self.alerts_dir = self.root / "alerts"

        self.reports_dir = self.root / "reports"
        self.deleted_reports_dir = self.root / "deleted_reports"
        self.detections_dir = self.root / "detections"
        self.snapshots_dir = self.root / "snapshots"

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.deleted_reports_dir.mkdir(parents=True, exist_ok=True)
        self.detections_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

        self.events_dir.mkdir(parents=True, exist_ok=True)
        self.statistics_dir.mkdir(parents=True, exist_ok=True)
        self.alerts_dir.mkdir(parents=True, exist_ok=True)

        self._lock = Lock()

        logger.info("Archive Storage initialized.")

    # =====================================================
    # Helpers
    # =====================================================

    def _today_file(
        self,
        folder: Path
    ) -> Path:

        filename = datetime.now().strftime("%Y-%m-%d.json")

        return folder / filename

    def _append(
        self,
        folder: Path,
        payload: Dict[str, Any]
    ):

        path = self._today_file(folder)

        with self._lock:

            if path.exists():

                try:

                    with open(path, "r", encoding="utf-8") as f:

                        data = json.load(f)

                except Exception:

                    data = []

            else:

                data = []

            payload["archived_at"] = datetime.utcnow().isoformat()

            data.append(payload)

            with open(path, "w", encoding="utf-8") as f:

                json.dump(
                    data,
                    f,
                    indent=4
                )

    def _load(
        self,
        folder: Path,
        date: str
    ) -> List[Dict]:

        path = folder / f"{date}.json"

        if not path.exists():

            return []

        with open(path, "r", encoding="utf-8") as f:

            return json.load(f)

    # =====================================================
    # Events
    # =====================================================

    def archive_event(
        self,
        event: Dict[str, Any]
    ):

        self._append(
            self.events_dir,
            event
        )

    def load_events(
        self,
        date: str
    ) -> List[Dict]:

        return self._load(
            self.events_dir,
            date
        )

    # =====================================================
    # Statistics
    # =====================================================

    def archive_statistics(
        self,
        statistics: Dict[str, Any]
    ):

        self._append(
            self.statistics_dir,
            statistics
        )

    def load_statistics(
        self,
        date: str
    ) -> List[Dict]:

        return self._load(
            self.statistics_dir,
            date
        )
    
    # =====================================================
    # Reports
    # =====================================================

    def archive_report(
        self,
        report: Dict[str, Any]
    ):

        self._append(
            self.reports_dir,
            report
        )


    def load_reports(
        self,
        date: str
    ) -> List[Dict]:

        return self._load(
            self.reports_dir,
            date
        )

    # =====================================================
    # Deleted Reports
    # =====================================================

    def archive_deleted_report(
        self,
        report: Dict[str, Any]
    ):

        payload = report.copy()

        payload["deleted_at"] = datetime.utcnow().isoformat()

        self._append(
            self.deleted_reports_dir,
            payload
        )


    def load_deleted_reports(
        self,
        date: str
    ) -> List[Dict]:

        return self._load(
            self.deleted_reports_dir,
            date
        )

    # =====================================================
    # Detections
    # =====================================================

    def archive_detection(
        self,
        detection: Dict[str, Any]
    ):

        self._append(
            self.detections_dir,
            detection
        )


    def load_detections(
        self,
        date: str
    ) -> List[Dict]:

        return self._load(
            self.detections_dir,
            date
        )
    
    # =====================================================
    # Snapshots
    # =====================================================

    def archive_snapshot(
        self,
        snapshot: Dict[str, Any]
    ):

        self._append(
            self.snapshots_dir,
            snapshot
        )


    def load_snapshots(
        self,
        date: str
    ) -> List[Dict]:

        return self._load(
            self.snapshots_dir,
            date
        )

    # =====================================================
    # Alerts
    # =====================================================

    def archive_alert(
        self,
        alert: Dict[str, Any]
    ):

        self._append(
            self.alerts_dir,
            alert
        )

    def load_alerts(
        self,
        date: str
    ) -> List[Dict]:

        return self._load(
            self.alerts_dir,
            date
        )

    # =====================================================
    # Cleanup
    # =====================================================

    def delete_archive(
        self,
        category: str,
        date: str
    ) -> bool:

        folders = {

            "events": self.events_dir,

            "statistics": self.statistics_dir,

            "alerts": self.alerts_dir,

            "reports": self.reports_dir,

            "deleted_reports": self.deleted_reports_dir,

            "detections": self.detections_dir,

            "snapshots": self.snapshots_dir

        }

        folder = folders.get(category)

        if folder is None:

            return False

        path = folder / f"{date}.json"

        if path.exists():

            path.unlink()

            logger.info(
                f"Deleted archive {path.name}"
            )

            return True

        return False

    # =====================================================
    # Metadata
    # =====================================================

    def info(self):

        return {

            "events_files":
                len(list(self.events_dir.glob("*.json"))),

            "statistics_files":
                len(list(self.statistics_dir.glob("*.json"))),

            "alerts_files":
                len(list(self.alerts_dir.glob("*.json"))),

            "reports_files":
                len(list(self.reports_dir.glob("*.json"))),

            "deleted_reports_files":
                len(list(self.deleted_reports_dir.glob("*.json"))),

            "detections_files":
                len(list(self.detections_dir.glob("*.json"))),

            "snapshots_files":
                len(list(self.snapshots_dir.glob("*.json"))),

            "root":
                str(self.root)

        }