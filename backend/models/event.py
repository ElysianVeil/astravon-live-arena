"""
============================================================
Astravon Live Arena
Event Model

Purpose:
    Database model representing an event.

Author:
    House of Astravon

Version:
    1.0.0
============================================================
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Float
)

from database.base import Base


class Event(Base):
    """
    Event database model.
    """

    __tablename__ = "events"

    # ========================================================
    # Primary Key
    # ========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ========================================================
    # Event Information
    # ========================================================

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    category = Column(
        String(50),
        nullable=False,
        default="Football"
    )

    venue = Column(
        String(150),
        nullable=False
    )

    mode = Column(
        String(50),
        nullable=False,
        default="football"
    )

    # ========================================================
    # Capacity
    # ========================================================

    capacity = Column(
        Integer,
        nullable=False,
        default=500
    )

    current_attendance = Column(
        Integer,
        nullable=False,
        default=0
    )

    # ========================================================
    # Event Status
    # ========================================================

    status = Column(
        String(30),
        nullable=False,
        default="scheduled"
    )

    is_active = Column(
        Boolean,
        default=False
    )

    # ========================================================
    # Environmental Information
    # ========================================================

    temperature = Column(
        Float,
        default=25.0
    )

    humidity = Column(
        Float,
        default=50.0
    )

    # ========================================================
    # Risk Information
    # ========================================================

    risk_level = Column(
        String(20),
        default="Low"
    )

    # ========================================================
    # Timestamps
    # ========================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ========================================================
    # String Representation
    # ========================================================

    def __repr__(self):

        return (
            f"<Event("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"status='{self.status}'"
            f")>"
        )