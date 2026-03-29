from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketRepository:
    """
    Repository responsible for direct ticket database operations.

    This layer should contain persistence logic only.
    It should not enforce business policy.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Ticket]:
        """
        Return all tickets from the database.
        """
        return self.db.query(Ticket).all()

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
