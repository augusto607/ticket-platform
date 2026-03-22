from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    """
    Return all tickets.

    Route responsibility:
    - receive the HTTP request
    - obtain required dependencies
    - call the service layer
    - return the response
    """
    repository = TicketRepository(db)
    service = TicketService(repository)

    return service.list_tickets()


@router.post("/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    Create a new ticket.

    Notice that the route does not directly talk SQL.
    It delegates to service -> repository.
    """
    repository = TicketRepository(db)
    service = TicketService(repository)

    try:
        return service.create_ticket(ticket)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
