from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.deps import get_ticket_service
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    status_filter: str | None = Query(
        default=None,
        alias="status",
        description="Optional filter by ticket status.",
    ),
    priority_filter: str | None = Query(
        default=None,
        alias="priority",
        description="Optional filter by ticket priority.",
    ),
    sort_by: str = Query(
        default="created_at",
        description="Field used to sort the returned tickets.",
    ),
    order: str = Query(
        default="desc",
        description="Sort direction: asc or desc.",
    ),
    service: TicketService = Depends(get_ticket_service),
):
    """
    Return tickets with optional filtering and sorting.

    Query parameter examples:
    - /tickets/?status=open
    - /tickets/?priority=high
    - /tickets/?sort_by=updated_at&order=asc
    - /tickets/?status=closed&priority=low
    """
    try:
        return service.list_tickets(
            status=status_filter,
            priority=priority_filter,
            sort_by=sort_by,
            order=order,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, service: TicketService = Depends(get_ticket_service)):
    """
    Return one ticket by ID.
    """
    ticket = service.get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} was not found.",
        )

    return ticket


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate,
    service: TicketService = Depends(get_ticket_service),
):
    """
    Create a new ticket.
    """
    try:
        return service.create_ticket(ticket)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    service: TicketService = Depends(get_ticket_service),
):
    """
    Update an existing ticket.

    PUT is used here as a full update endpoint, but because the schema fields
    are optional, the practical behavior is closer to a partial update.
    For now this is acceptable for learning. Later we can split PUT vs PATCH
    more explicitly if we want stricter REST semantics.
    """
    try:
        updated_ticket = service.update_ticket(ticket_id, ticket_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if updated_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} was not found.",
        )

    return updated_ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service),
):
    """
    Delete an existing ticket.

    A 204 response means the deletion succeeded and there is no response body.
    """
    deleted = service.delete_ticket(ticket_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} was not found.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
