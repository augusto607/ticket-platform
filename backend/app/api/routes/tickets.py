from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.deps import get_current_user, get_ticket_service
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
    current_user=Depends(get_current_user),
):
    """
    Return only the authenticated user's tickets,
    with optional filtering and sorting.
    """
    try:
        return service.list_tickets(
            owner_id=current_user.id,
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
def get_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service),
    current_user=Depends(get_current_user),
):
    """
    Return one ticket by ID only if it belongs to the authenticated user.
    """
    ticket = service.get_ticket(ticket_id, owner_id=current_user.id)

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
    current_user=Depends(get_current_user),
):
    """
    Create a new ticket owned by the authenticated user.
    """
    try:
        return service.create_ticket(ticket, owner_id=current_user.id)
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
    current_user=Depends(get_current_user),
):
    """
    Update an existing ticket only if it belongs to the authenticated user.
    """
    try:
        updated_ticket = service.update_ticket(
            ticket_id=ticket_id,
            owner_id=current_user.id,
            ticket_data=ticket_data,
        )
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
    current_user=Depends(get_current_user),
):
    """
    Delete an existing ticket only if it belongs to the authenticated user.
    """
    deleted = service.delete_ticket(
        ticket_id=ticket_id, owner_id=current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} was not found.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
