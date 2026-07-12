"""
============================================================
Astravon Live Arena
Common Schemas

Purpose:
    Shared Pydantic schemas used throughout
    the backend.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# Base Schema
# ============================================================

class AstravonSchema(BaseModel):
    """
    Base schema for all Pydantic models.
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )


# ============================================================
# Success Response
# ============================================================

class SuccessResponse(AstravonSchema):
    """
    Standard success response.
    """

    success: bool = True

    message: str

    data: Optional[Any] = None


# ============================================================
# Error Response
# ============================================================

class ErrorResponse(AstravonSchema):
    """
    Standard error response.
    """

    success: bool = False

    message: str

    data: Optional[Any] = None


# ============================================================
# Pagination
# ============================================================

class Pagination(AstravonSchema):
    """
    Pagination information.
    """

    page: int = 1

    page_size: int = 10

    total_records: int = 0

    total_pages: int = 0


# ============================================================
# Health Response
# ============================================================

class HealthResponse(AstravonSchema):
    """
    Health check response.
    """

    success: bool = True

    service: str

    version: str

    status: str

    timestamp: datetime


# ============================================================
# Message Response
# ============================================================

class MessageResponse(AstravonSchema):
    """
    Simple message response.
    """

    success: bool = True

    message: str


# ============================================================
# Identifier
# ============================================================

class Identifier(AstravonSchema):
    """
    Generic identifier schema.
    """

    id: int


# ============================================================
# Timestamp
# ============================================================

class Timestamp(AstravonSchema):
    """
    Timestamp schema.
    """

    created_at: datetime

    updated_at: Optional[datetime] = None