from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    """
    Schema used when creating a new ticket.
    """
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    priority: str = "medium"


class TicketUpdate(BaseModel):
    """
    Schema used when updating an existing ticket.

    All fields are optional because the client may update
    only part of the ticket.
    """
    title: Optional[str] = Field(default=None, min_length=3, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TicketResponse(BaseModel):
    """
    Schema returned to the client when a ticket is read or created.
    """
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
