from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService


def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    """
    Dependency that provides a TicketRepository instance.

    FastAPI will:
    - call get_db()
    - inject the DB session
    - create the repository
    """
    return TicketRepository(db)


def get_ticket_service(
    repository: TicketRepository = Depends(get_ticket_repository),
) -> TicketService:
    """
    Dependency that provides a TicketService instance.

    Notice:
    - it depends on the repository
    - FastAPI resolves dependencies automatically
    """
    return TicketService(repository)
