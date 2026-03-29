from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    """
    Service layer responsible for ticket-related business logic.

    This is where business rules belong.
    """

    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def list_tickets(self):
        """
        Return all tickets.
        """
        return self.repository.get_all()

    def get_ticket(self, ticket_id: int):
        """
        Return a single ticket by ID.

        The service does not raise HTTP errors directly.
        It returns None if the ticket does not exist,
        and the route decides how to map that to HTTP.
        """
        return self.repository.get_by_id(ticket_id)

    def create_ticket(self, ticket_data: TicketCreate):
        """
        Validate business rules before creating a ticket.
        """
        allowed_priorities = {"low", "medium", "high"}

        normalized_priority = ticket_data.priority.lower()

        if normalized_priority not in allowed_priorities:
            raise ValueError(
                f"Invalid priority '{ticket_data.priority}'. "
                f"Allowed values: {allowed_priorities}"
            )

        ticket_data.priority = normalized_priority

        return self.repository.create(ticket_data)

    def update_ticket(self, ticket_id: int, ticket_data: TicketUpdate):
        """
        Update an existing ticket after validating business rules.
        """
        ticket = self.repository.get_by_id(ticket_id)

        if ticket is None:
            return None

        allowed_priorities = {"low", "medium", "high"}
        allowed_statuses = {"open", "in_progress", "closed"}

        if ticket_data.priority is not None:
            normalized_priority = ticket_data.priority.lower()

            if normalized_priority not in allowed_priorities:
                raise ValueError(
                    f"Invalid priority '{ticket_data.priority}'. "
                    f"Allowed values: {allowed_priorities}"
                )

            ticket_data.priority = normalized_priority

        if ticket_data.status is not None:
            normalized_status = ticket_data.status.lower()

            if normalized_status not in allowed_statuses:
                raise ValueError(
                    f"Invalid status '{ticket_data.status}'. "
                    f"Allowed values: {allowed_statuses}"
                )

            ticket_data.status = normalized_status

        return self.repository.update(ticket, ticket_data)
