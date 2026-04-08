from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.core.db import Base


def utc_now() -> datetime:
    """
    Return the current UTC time as a timezone-aware datetime.
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

    # Foreign key pointing to the user who owns this ticket.
    # This is the foundation for authorization rules.
    owner_id = Column(Integer, ForeignKey("users.id"),
                      nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
