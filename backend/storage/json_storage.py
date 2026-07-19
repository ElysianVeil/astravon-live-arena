"""
============================================================
Astravon Live Arena
JSON Storage

Purpose
-------
Persistent JSON storage layer used by the backend before a
database is introduced.

Features
--------
- Thread-safe
- Automatic directory creation
- Automatic file creation
- Atomic writes
- Read / Write JSON
- Append records
- Update records
- Delete records
- Backup support
- Generic enough to support:
    • Cameras
    • Alerts
    • Statistics
    • Reports
    • Events

Author:
    House of Astravon
============================================================
"""

from __future__ import annotations

import json
import shutil
import threading

from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional


class JSONStorage:
    """
    Generic JSON persistence layer.

    Every storage file contains either

        {}

    or

        []

    depending on how you initialize it.
    """

    def __init__(
        self,
        filepath: str,
        default: Any = None
    ):

        self.filepath = Path(filepath)

        self.lock = threading.Lock()

        if default is None:
            default = {}

        self.default = default

        self._ensure_exists()

    # =====================================================
    # Initialization
    # =====================================================

    def _ensure_exists(self):

        self.filepath.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.filepath.exists():

            with open(
                self.filepath,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.default,
                    f,
                    indent=4
                )

    # =====================================================
    # Read
    # =====================================================

    def load(self):

        with self.lock:

            try:

                with open(
                    self.filepath,
                    "r",
                    encoding="utf-8"
                ) as f:

                    return json.load(f)

            except Exception:

                return self.default

    # =====================================================
    # Save
    # =====================================================

    def save(
        self,
        data
    ):

        with self.lock:

            tmp = self.filepath.with_suffix(".tmp")

            with open(
                tmp,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            tmp.replace(self.filepath)

    # =====================================================
    # Dictionary Operations
    # =====================================================

    def get(
        self,
        key,
        default=None
    ):

        data = self.load()

        return data.get(
            key,
            default
        )

    def set(
        self,
        key,
        value
    ):

        data = self.load()

        data[key] = value

        self.save(data)

    def delete(
        self,
        key
    ):

        data = self.load()

        if key in data:

            del data[key]

            self.save(data)

    def update(
        self,
        values: Dict
    ):

        data = self.load()

        data.update(values)

        self.save(data)

    # =====================================================
    # List Operations
    # =====================================================

    def append(
        self,
        record
    ):

        data = self.load()

        if not isinstance(data, list):

            raise TypeError(
                "Storage is not a list."
            )

        data.append(record)

        self.save(data)

    def extend(
        self,
        records
    ):

        data = self.load()

        if not isinstance(data, list):

            raise TypeError(
                "Storage is not a list."
            )

        data.extend(records)

        self.save(data)

    def remove(
        self,
        index
    ):

        data = self.load()

        if not isinstance(data, list):

            raise TypeError(
                "Storage is not a list."
            )

        if 0 <= index < len(data):

            data.pop(index)

            self.save(data)

    # =====================================================
    # Utilities
    # =====================================================

    def clear(self):

        self.save(self.default)

    def exists(self):

        return self.filepath.exists()

    def backup(self):

        """
        Creates

        filename_YYYYMMDD_HHMMSS.json
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup = self.filepath.with_name(

            f"{self.filepath.stem}_{timestamp}.json"

        )

        shutil.copy2(
            self.filepath,
            backup
        )

        return backup

    def size(self):

        return self.filepath.stat().st_size

    # =====================================================
    # Context Manager
    # =====================================================

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):

        return False


# ============================================================
# Default Storage Files
# ============================================================

alerts_storage = JSONStorage(
    "data/alerts.json",
    default=[]
)

statistics_storage = JSONStorage(
    "data/statistics.json",
    default={}
)

events_storage = JSONStorage(
    "data/events.json",
    default=[]
)

reports_storage = JSONStorage(
    "data/reports.json",
    default=[]
)

cameras_storage = JSONStorage(
    "data/cameras.json",
    default={}
)