"""
============================================================
Astravon Live Arena
Logger

Purpose:
    Centralized logging configuration for the
    backend application.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

import logging
import sys
from ..config import LOG_LEVEL


# ============================================================
# Logger Factory
# ============================================================

def get_logger(
    name: str = "astravon"
) -> logging.Logger:
    """
    Returns a configured logger.

    Args:
        name:
            Logger name.

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:

        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(

        "[%(asctime)s] "
        "[%(levelname)s] "
        "[%(name)s] "
        "%(message)s"

    )

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    logger.propagate = False

    return logger


# ============================================================
# Default Logger
# ============================================================

logger = get_logger()