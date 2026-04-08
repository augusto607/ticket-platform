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
        owner_id: int,
        status: str | None = None,
        priority: str | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ):
        """
        Return tickets for one specific owner using optional filters and sorting.
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

        return self.repository.get_all_by_owner(
            owner_id=owner_id,
            status=normalized_status,
            priority=normalized_priority,
            sort_by=sort_by,
            order=normalized_order,
        )

    def get_ticket(self, ticket_id: int, owner_id: int):
        """
        Return one ticket only if it belongs to the specified owner.
        """
        return self.repository.get_by_id_and_owner(ticket_id, owner_id)

    def create_ticket(self, ticket_data: TicketCreate, owner_id: int):
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

        return self.repository.create(ticket_data, owner_id)

    def update_ticket(self, ticket_id: int, owner_id: int, ticket_data: TicketUpdate):
        """
        Update an existing ticket only if it belongs to the specified owner.
        """
        ticket = self.repository.get_by_id_and_owner(ticket_id, owner_id)

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

    def delete_ticket(self, ticket_id: int, owner_id: int) -> bool:
        """
        Delete a ticket only if it belongs to the specified owner.
        """
        ticket = self.repository.get_by_id_and_owner(ticket_id, owner_id)

        if ticket is None:
            return False

        self.repository.delete(ticket)
        return True
