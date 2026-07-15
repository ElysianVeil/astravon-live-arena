"""
============================================================
Astravon Live Arena
Configuration

Author: House of Astravon
Version: 1.0.0
============================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Astravon Live Arena"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"

    PORT: int = 8000


    DATABASE_URL: str = (
        "postgresql://postgres:password@localhost/"
        "astravon_live_arena"
    )


    AI_ENGINE_URL: str = (
        "http://127.0.0.1:9000"
    )


    LOG_LEVEL: str = "INFO"


    ENABLE_SIMULATION: bool = True

    ENABLE_DATABASE: bool = True

    ENABLE_WEBSOCKET: bool = False

    ENABLE_REPORTS: bool = True

    # ------------------------------------------------------
    # CORS
    # ------------------------------------------------------

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]

# ----------------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

settings = Settings()

# ----------------------------------------------------------
# Project Information
# ----------------------------------------------------------

PROJECT_NAME = "Astravon Live Arena"

PROJECT_VERSION = "1.0.0"

PROJECT_AUTHOR = "House of Astravon"

PROJECT_DESCRIPTION = (
    "AI-powered crowd monitoring and event safety platform."
)

# ----------------------------------------------------------
# Application
# ----------------------------------------------------------

DEBUG = os.getenv("DEBUG", "True") == "True"

HOST = os.getenv("HOST", "127.0.0.1")

PORT = int(os.getenv("PORT", 8000))

# ----------------------------------------------------------
# Database
# ----------------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost/astravon_live_arena"
)

# ----------------------------------------------------------
# AI Engine
# ----------------------------------------------------------

AI_ENGINE_URL = os.getenv(
    "AI_ENGINE_URL",
    "http://127.0.0.1:9000"
)

# ----------------------------------------------------------
# WebSocket
# ----------------------------------------------------------

WEBSOCKET_URL = os.getenv(
    "WEBSOCKET_URL",
    "ws://127.0.0.1:8000/ws"
)

# ----------------------------------------------------------
# Security
# ----------------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "CHANGE_THIS_SECRET_KEY"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

# ----------------------------------------------------------
# CORS
# ----------------------------------------------------------

ALLOWED_ORIGINS = settings.ALLOWED_ORIGINS

# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

LOG_DIRECTORY = BASE_DIR / "logs"

LOG_DIRECTORY.mkdir(exist_ok=True)

# ----------------------------------------------------------
# Event Defaults
# ----------------------------------------------------------

# DEFAULT_EVENT_NAME = "Football Match"

# DEFAULT_VENUE = "Arena A"

# DEFAULT_CAPACITY = 500

# ----------------------------------------------------------
# AI Thresholds
# ----------------------------------------------------------

# LOW_DENSITY_THRESHOLD = 30

# MEDIUM_DENSITY_THRESHOLD = 80

# HIGH_DENSITY_THRESHOLD = 120

# LOW_RISK_THRESHOLD = 30

# MEDIUM_RISK_THRESHOLD = 60

# HIGH_RISK_THRESHOLD = 80

# ----------------------------------------------------------
# Heat Simulation
# ----------------------------------------------------------

# DEFAULT_TEMPERATURE = 25.0

# DEFAULT_HUMIDITY = 50.0

# DEFAULT_HEAT_INDEX = 27.0

# ----------------------------------------------------------
# API
# ----------------------------------------------------------

API_PREFIX = "/api"

API_VERSION = "v1"

# ----------------------------------------------------------
# Uploads
# ----------------------------------------------------------

UPLOAD_FOLDER = BASE_DIR / "uploads"

UPLOAD_FOLDER.mkdir(exist_ok=True)

# ----------------------------------------------------------
# Reports
# ----------------------------------------------------------

REPORT_FOLDER = BASE_DIR / "reports"

REPORT_FOLDER.mkdir(exist_ok=True)

# ----------------------------------------------------------
# Models
# ----------------------------------------------------------

MODEL_DIRECTORY = BASE_DIR.parent / "ai_engine" / "models"

YOLO_MODEL = MODEL_DIRECTORY / "yolov_model" / "yolov8n.pt"

# ----------------------------------------------------------
# Camera
# ----------------------------------------------------------

# DEFAULT_CAMERA_INDEX = 0

# FRAME_WIDTH = 1280

# FRAME_HEIGHT = 720

# FPS = 30

# ----------------------------------------------------------
# Development Flags
# ----------------------------------------------------------

ENABLE_SIMULATION = True

ENABLE_DATABASE = True

ENABLE_WEBSOCKET = False

ENABLE_REPORTS = True

ENABLE_LOGGING = True

# ----------------------------------------------------------
# Helper Function
# ----------------------------------------------------------

def print_configuration():
    """
    Prints the current application configuration.
    Useful during development.
    """

    print("=" * 55)
    print(PROJECT_NAME)
    print("=" * 55)

    print(f"Version        : {PROJECT_VERSION}")
    print(f"Debug          : {DEBUG}")
    print(f"Host           : {HOST}")
    print(f"Port           : {PORT}")
    print(f"Database       : {DATABASE_URL}")
    print(f"AI Engine      : {AI_ENGINE_URL}")
    # print(f"Camera Index   : {DEFAULT_CAMERA_INDEX}")
    print(f"Simulation     : {ENABLE_SIMULATION}")
    print(f"Reports        : {ENABLE_REPORTS}")
    print("=" * 55)


# ----------------------------------------------------------
# Entry Point
# ----------------------------------------------------------

if __name__ == "__main__":
    print_configuration()