"""
============================================================
Astravon Live Arena
Backend Entry Point

Author: House of Astravon
Version: 1.0.0
============================================================
"""

from fastapi import FastAPI

from backend.middleware._init_ import (
    configure_cors,
    register_exception_handlers,
    LoggingMiddleware
)

from backend.api.router import api_router


# ============================================================
# Application Creation
# ============================================================

app = FastAPI(

    title="Astravon Live Arena API",

    description=(
        "AI-powered crowd monitoring "
        "and event safety platform."
    ),

    version="1.0.0"
)



# ============================================================
# Middleware Configuration
# ============================================================

configure_cors(app)


app.add_middleware(
    LoggingMiddleware
)



# ============================================================
# Exception Handling
# ============================================================

register_exception_handlers(app)



# ============================================================
# API Registration
# ============================================================

app.include_router(
    api_router
)



# ============================================================
# Root Endpoint
# ============================================================

@app.get(
    "/",
    tags=["General"]
)
async def home():

    return {

        "project": "Astravon Live Arena",

        "version": "1.0.0",

        "status": "Running"

    }



# ============================================================
# Application Health
# ============================================================

@app.get(
    "/health",
    tags=["General"]
)
async def health():

    return {

        "success": True,

        "message": "Backend healthy",

        "service": "Astravon Live Arena"

    }