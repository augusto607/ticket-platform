from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import decode_access_token
from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.services.ticket_service import TicketService

# This tells FastAPI how clients are expected to send the token.
# "tokenUrl" points to the login endpoint that issues tokens.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    """
    Provide a TicketRepository instance.
    """
    return TicketRepository(db)


def get_ticket_service(
    repository: TicketRepository = Depends(get_ticket_repository),
) -> TicketService:
    """
    Provide a TicketService instance.
    """
    return TicketService(repository)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Provide a UserRepository instance.
    """
    return UserRepository(db)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
):
    """
    Resolve the currently authenticated user from the JWT access token.

    Flow:
    1. Read the Bearer token from the Authorization header
    2. Decode and validate the JWT
    3. Extract the user identity from the token payload
    4. Load the user from the database
    5. Reject the request if token or user is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)

        # "sub" is the subject field we stored when creating the token.
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = user_repository.get_by_email(email)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account.",
        )

    return user
