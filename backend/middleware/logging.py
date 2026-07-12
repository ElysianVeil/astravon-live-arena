"""
============================================================
Astravon Live Arena
Logging Middleware

Purpose:
    Logs incoming requests and outgoing responses.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from backend.utils.logger import get_logger
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# ============================================================
# Logger Configuration
# ============================================================

logger = get_logger(
    "HTTP"
)



# ============================================================
# Logging Middleware
# ============================================================

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every HTTP request and response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        start_time = time.time()

        logger.info(
            f"Incoming Request: "
            f"{request.method} {request.url.path}"
        )

        response = await call_next(request)

        duration = round(
            time.time() - start_time,
            4
        )

        logger.info(
            f"Completed "
            f"{request.method} "
            f"{request.url.path} "
            f"Status={response.status_code} "
            f"Duration={duration}s"
        )

        response.headers["X-Process-Time"] = str(duration)

        return response