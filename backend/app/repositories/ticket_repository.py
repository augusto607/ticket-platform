from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketRepository:
    """
    Repository responsible for direct ticket database operations.

    This layer contains persistence logic only.
    It should not contain business rules.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all_by_owner(
        self,
        owner_id: int,
        status: str | None = None,
        priority: str | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> list[Ticket]:
        """
        Return tickets owned by a specific user, with optional filtering and sorting.
        """
        query = self.db.query(Ticket).filter(Ticket.owner_id == owner_id)

        if status is not None:
            query = query.filter(Ticket.status == status)

        if priority is not None:
            query = query.filter(Ticket.priority == priority)

        sortable_columns = {
            "id": Ticket.id,
            "title": Ticket.title,
            "status": Ticket.status,
            "priority": Ticket.priority,
            "created_at": Ticket.created_at,
            "updated_at": Ticket.updated_at,
        }

        sort_column = sortable_columns[sort_by]
        sort_expression = asc(
            sort_column) if order == "asc" else desc(sort_column)

        return query.order_by(sort_expression).all()

    def get_by_id_and_owner(self, ticket_id: int, owner_id: int) -> Ticket | None:
        """
        Return one ticket by ID only if it belongs to the specified owner.
        """
        return (
            self.db.query(Ticket)
            .filter(Ticket.id == ticket_id, Ticket.owner_id == owner_id)
            .first()
        )

    def create(self, ticket_data: TicketCreate, owner_id: int) -> Ticket:
        """
        Create a new ticket record owned by the specified user.
        """
        ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            status="open",
            owner_id=owner_id,
        )

        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)

        return ticket

    def update(self, ticket: Ticket, ticket_data: TicketUpdate) -> Ticket:
        """
        Update an existing ticket record.

        Only fields explicitly provided by the client will be updated.
        """
        update_data = ticket_data.model_dump(exclude_unset=True)

        for field_name, field_value in update_data.items():
            setattr(ticket, field_name, field_value)

        self.db.commit()
        self.db.refresh(ticket)

        return ticket

    def delete(self, ticket: Ticket) -> None:
        """
        Delete an existing ticket record from the database.
        """
        self.db.delete(ticket)
        self.db.commit()
