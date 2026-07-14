"""
============================================================
Astravon Live Arena
Logger Utility

Purpose:
    Configures centralized logging for the AI Engine.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from __future__ import annotations

import logging
from pathlib import Path

from config import settings


# ============================================================
# Log Directory
# ============================================================

LOG_DIRECTORY = Path(settings.LOG_DIRECTORY)

LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIRECTORY / "ai_engine.log"


# ============================================================
# Logger Configuration
# ============================================================

logger = logging.getLogger("astravon.ai")

if not logger.handlers:

    logger.setLevel(
        getattr(
            logging,
            settings.LOG_LEVEL.upper(),
            logging.INFO
        )
    )

    formatter = logging.Formatter(
        "[%(asctime)s] "
        "[%(levelname)s] "
        "[%(name)s] "
        "%(message)s"
    )

    # --------------------------------------------------------
    # Console Handler
    # --------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # --------------------------------------------------------
    # File Handler
    # --------------------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

# ============================================================
# Logger Factory
# ============================================================

def get_logger(name: str) -> logging.Logger:
    """
    Returns a child logger using the shared configuration.

    Parameters
    ----------
    name:
        Module or component name.

    Returns
    -------
    logging.Logger
    """

    child_logger = logging.getLogger(f"astravon.ai.{name}")

    if not child_logger.handlers:
        child_logger.setLevel(logger.level)

        for handler in logger.handlers:
            child_logger.addHandler(handler)

        child_logger.propagate = False

    return child_logger


# ============================================================
# Helper Functions
# ============================================================

def debug(message: str) -> None:
    """
    Logs a debug message.
    """

    logger.debug(message)


def info(message: str) -> None:
    """
    Logs an informational message.
    """

    logger.info(message)


def warning(message: str) -> None:
    """
    Logs a warning message.
    """

    logger.warning(message)


def error(message: str) -> None:
    """
    Logs an error message.
    """

    logger.error(message)


def exception(message: str) -> None:
    """
    Logs an exception with traceback.
    """

    logger.exception(message)


# ============================================================
# Startup Log
# ============================================================

logger.info("=" * 60)
logger.info("Astravon Live Arena AI Engine Logger Initialized")
logger.info("=" * 60)