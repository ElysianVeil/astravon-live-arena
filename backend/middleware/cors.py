"""
============================================================
Astravon Live Arena
CORS Configuration

Purpose:
    Configures Cross-Origin Resource Sharing (CORS)
    for the FastAPI application.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import settings


# ============================================================
# Configure CORS
# ============================================================

def configure_cors(
    app: FastAPI
) -> None:
    """
    Configures CORS middleware.

    Args:
        app: FastAPI application instance.
    """

    app.add_middleware(
        CORSMiddleware,

        allow_origins=settings.ALLOWED_ORIGINS,

        allow_credentials=True,

        allow_methods=[
            "*"
        ],

        allow_headers=[
            "*"
        ],

        expose_headers=[
            "X-Process-Time"
        ]
    )