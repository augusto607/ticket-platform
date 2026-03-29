from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    """
    Service layer responsible for ticket-related business logic.

    This is where business rules belong.
    """

    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def list_tickets(
        self,
        status: str | None = None,
        priority: str | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ):
        """
        Return tickets using optional filters and sorting.

        The service validates client-friendly inputs before delegating
        to the repository.
        """
        allowed_statuses = {"open", "in_progress", "closed"}
        allowed_priorities = {"low", "medium", "high"}
        allowed_sort_fields = {
            "id",
            "title",
            "status",
            "priority",
            "created_at",
            "updated_at",
        }
        allowed_order_values = {"asc", "desc"}

        normalized_status = None
        if status is not None:
            normalized_status = status.lower()

            if normalized_status not in allowed_statuses:
                raise ValueError(
                    f"Invalid status '{status}'. Allowed values: {allowed_statuses}"
                )

        normalized_priority = None
        if priority is not None:
            normalized_priority = priority.lower()

            if normalized_priority not in allowed_priorities:
                raise ValueError(
                    f"Invalid priority '{priority}'. Allowed values: {allowed_priorities}"
                )

        if sort_by not in allowed_sort_fields:
            raise ValueError(
                f"Invalid sort_by '{sort_by}'. Allowed values: {allowed_sort_fields}"
            )

        normalized_order = order.lower()
        if normalized_order not in allowed_order_values:
            raise ValueError(
                f"Invalid order '{order}'. Allowed values: {allowed_order_values}"
            )

        return self.repository.get_all(
            status=normalized_status,
            priority=normalized_priority,
            sort_by=sort_by,
            order=normalized_order,
        )

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

    def delete_ticket(self, ticket_id: int) -> bool:
        """
        Delete a ticket by ID.

        Returns:
        - True if the ticket existed and was deleted
        - False if the ticket was not found
        """
        ticket = self.repository.get_by_id(ticket_id)

        if ticket is None:
            return False

        self.repository.delete(ticket)
        return True
