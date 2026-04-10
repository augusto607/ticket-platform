from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash

from app.core.config import settings

# Create a password hasher using Argon2.
# This is a modern password hashing choice for new systems.
password_hash = PasswordHash.recommended()


def utc_now() -> datetime:
    """
    Return the current UTC time as a timezone-aware datetime.
    """
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password before storing it.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against the stored password hash.
    """
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Create a signed JWT access token.

    The payload contains:
    - sub: token subject (the user email in this project)
    - exp: expiration timestamp
    """
    expires_at = utc_now() + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Returns the decoded payload if valid.
    Raises an error if the token is invalid, expired, or malformed.
    """
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
