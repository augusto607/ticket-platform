from sqlalchemy import Column, Integer, String, Text

from app.core.db import Base


class Ticket(Base):
    """
    SQLAlchemy model representing the tickets table in PostgreSQL.
    """

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    # Short title for the ticket
    title = Column(String(255), nullable=False)

    # Longer optional description
    description = Column(Text, nullable=True)

    # Current workflow status
    status = Column(String(50), nullable=False, default="open")

    # Business priority level
    priority = Column(String(50), nullable=False, default="medium")
