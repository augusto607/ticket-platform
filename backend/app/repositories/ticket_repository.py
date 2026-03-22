from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate


class TicketRepository:
    """
    Repository layer responsible for direct database operations.

    This class should NOT contain business rules.
    Its job is to talk to the database.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        """
        Return all tickets from the database.
        """
        return self.db.query(Ticket).all()

    def create(self, ticket_data: TicketCreate):
        """
        Create and persist a new ticket record.
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
