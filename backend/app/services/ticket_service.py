from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate


class TicketService:
    """
    Service layer responsible for business logic.

    This is where workflow rules should live.
    Example:
    - validating allowed priorities
    - assigning default statuses
    - enforcing business constraints
    """

    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def list_tickets(self):
        """
        Return all tickets.

        Right now this is simple passthrough logic,
        but later business rules can be added here.
        """
        return self.repository.get_all()

    def create_ticket(self, ticket_data: TicketCreate):
        """
        Create a ticket using business-layer orchestration.
        """
        allowed_priorities = {"low", "medium", "high"}

        if ticket_data.priority not in allowed_priorities:
            raise ValueError(
                f"Invalid priority '{ticket_data.priority}'. "
                f"Allowed values: {allowed_priorities}"
            )

        return self.repository.create(ticket_data)
