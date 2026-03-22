from typing import Optional

from pydantic import BaseModel


class TicketCreate(BaseModel):
    """
    Schema used when the client wants to create a new ticket.
    """
    title: str
    description: Optional[str] = None
    priority: str = "medium"


class TicketResponse(BaseModel):
    """
    Schema returned to the client after reading or creating a ticket.
    """
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str

    class Config:
        from_attributes = True
