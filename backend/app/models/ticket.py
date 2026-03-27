from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.db import Base


def utc_now():
    """
    Returns the current UTC time as a timezone-aware datetime.

    Using a function ensures SQLAlchemy calls it at runtime
    for each row, not once at import time.
    """
    return datetime.now(timezone.utc)


class Ticket(Base):
    """
    SQLAlchemy model representing the tickets table.
    """

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    status = Column(String(50), nullable=False, default="open")

    priority = Column(String(50), nullable=False, default="medium")

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now,   # ✅ pass function, not value
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,   # ✅ same here
        onupdate=utc_now,  # ✅ called on update
        nullable=False,
    )
