from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_ticket_service
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/", response_model=list[TicketResponse])
def list_tickets(service: TicketService = Depends(get_ticket_service)):
    """
    Clean route:
    - No manual object creation
    - Just receives the service
    """
    return service.list_tickets()


@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    service: TicketService = Depends(get_ticket_service),
):
    """
    Clean route:
    - Delegates logic to the service
    - Handles only HTTP concerns
    """
    try:
        return service.create_ticket(ticket)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
