"""
============================================================
Astravon Live Arena
Pytest Configuration

Purpose:
    Shared test fixtures.

============================================================
"""

import pytest

from fastapi.testclient import TestClient

from backend.main import app



@pytest.fixture
def client():

    """
    FastAPI test client.
    """

    return TestClient(app)