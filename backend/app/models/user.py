from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.db import Base


def utc_now() -> datetime:
    """
    Return the current UTC time as a timezone-aware datetime.

    This function is used as a callable by SQLAlchemy so the value
    is generated at row creation time, not at import time.
    """
    return datetime.now(timezone.utc)


class User(Base):
    """
    SQLAlchemy model representing application users.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Email is used as the login identifier
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Optional display name for UI usage
    full_name = Column(String(255), nullable=False)

    # Securely hashed password, never plain text
    hashed_password = Column(String(255), nullable=False)

    # Useful for future admin / disable-user logic
    is_active = Column(Boolean, default=True, nullable=False)

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
