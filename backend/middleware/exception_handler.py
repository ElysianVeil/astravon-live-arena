"""
============================================================
Astravon Live Arena
Exception Handler

Purpose:
    Provides centralized exception handling for
    FastAPI applications.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from backend.utils.logger import get_logger

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


# ============================================================
# Logger
# ============================================================

logger = get_logger("ExceptionHandler")


# ============================================================
# HTTP Exceptions
# ============================================================

async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    """
    Handles HTTP exceptions.
    """

    logger.warning(
        f"HTTP {exc.status_code}: "
        f"{request.method} "
        f"{request.url.path}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None
        }
    )


# ============================================================
# Validation Exceptions
# ============================================================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Handles request validation errors.
    """

    logger.warning(
        f"Validation Error: "
        f"{request.method} "
        f"{request.url.path}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation failed.",
            "errors": exc.errors(),
            "data": None
        }
    )


# ============================================================
# Internal Server Error
# ============================================================

async def internal_server_error_handler(
    request: Request,
    exc: Exception
):
    """
    Handles unexpected exceptions.
    """

    logger.exception(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal Server Error.",
            "data": None
        }
    )


# ============================================================
# Register Handlers
# ============================================================

def register_exception_handlers(
    app: FastAPI
):
    """
    Registers all application exception handlers.
    """

    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler
    )

    app.add_exception_handler(
        Exception,
        internal_server_error_handler
    )