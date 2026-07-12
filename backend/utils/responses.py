"""
============================================================
Astravon Live Arena
Response Utilities

Purpose:
    Provides standardized API response helpers.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from typing import Any, Optional

from fastapi.responses import JSONResponse

from utils.constants import (

    SUCCESS_MESSAGE,

    ERROR_MESSAGE,

    NOT_FOUND_MESSAGE,

    VALIDATION_MESSAGE,

    SERVER_ERROR_MESSAGE

)


# ============================================================
# Success Response
# ============================================================

def success_response(
    data: Optional[Any] = None,
    message: str = SUCCESS_MESSAGE,
    status_code: int = 200
) -> JSONResponse:
    """
    Creates a standard success response.
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )


# ============================================================
# Error Response
# ============================================================

def error_response(
    message: str = ERROR_MESSAGE,
    status_code: int = 400,
    data: Optional[Any] = None
) -> JSONResponse:
    """
    Creates a standard error response.
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": data
        }
    )


# ============================================================
# Created Response
# ============================================================

def created_response(
    data: Optional[Any] = None,
    message: str = "Resource created successfully."
) -> JSONResponse:
    """
    Returns a HTTP 201 response.
    """

    return success_response(
        data=data,
        message=message,
        status_code=201
    )


# ============================================================
# Accepted Response
# ============================================================

def accepted_response(
    data: Optional[Any] = None,
    message: str = "Request accepted."
) -> JSONResponse:
    """
    Returns a HTTP 202 response.
    """

    return success_response(
        data=data,
        message=message,
        status_code=202
    )


# ============================================================
# No Content Response
# ============================================================

def no_content_response() -> JSONResponse:
    """
    Returns a HTTP 204 response.
    """

    return JSONResponse(
        status_code=204,
        content={}
    )


# ============================================================
# Not Found Response
# ============================================================

def not_found_response(
    message: str = NOT_FOUND_MESSAGE
) -> JSONResponse:
    """
    Returns a HTTP 404 response.
    """

    return error_response(
        message=message,
        status_code=404
    )


# ============================================================
# Validation Error Response
# ============================================================

def validation_response(
    errors: Any,
    message: str = VALIDATION_MESSAGE
) -> JSONResponse:
    """
    Returns a HTTP 422 response.
    """

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": message,
            "errors": errors,
            "data": None
        }
    )


# ============================================================
# Internal Server Error Response
# ============================================================

def server_error_response(
    message: str = SERVER_ERROR_MESSAGE
) -> JSONResponse:
    """
    Returns a HTTP 500 response.
    """

    return error_response(
        message=message,
        status_code=500
    )