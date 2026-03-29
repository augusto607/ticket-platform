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

    def get_all(
        self,
        status: str | None = None,
        priority: str | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> list[Ticket]:
        """
        Return tickets from the database with optional filtering and sorting.

        Parameters:
        - status: optional workflow status filter
        - priority: optional priority filter
        - sort_by: field used for sorting
        - order: ascending or descending sort direction
        """
        query = self.db.query(Ticket)

        # Apply filtering only if the client provided a status value
        if status is not None:
            query = query.filter(Ticket.status == status)

        # Apply filtering only if the client provided a priority value
        if priority is not None:
            query = query.filter(Ticket.priority == priority)

        # Map user-friendly sort field names to actual SQLAlchemy model columns
        sortable_columns = {
            "id": Ticket.id,
            "title": Ticket.title,
            "status": Ticket.status,
            "priority": Ticket.priority,
            "created_at": Ticket.created_at,
            "updated_at": Ticket.updated_at,
        }

        # Select the column requested by the client
        sort_column = sortable_columns[sort_by]

        # Build ascending or descending SQL sort expression
        sort_expression = asc(
            sort_column) if order == "asc" else desc(sort_column)

        return query.order_by(sort_expression).all()

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        """
        Return one ticket by its ID, or None if not found.
        """
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def create(self, ticket_data: TicketCreate) -> Ticket:
        """
        Create a new ticket record in the database.
        """
        ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            status="open",
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
