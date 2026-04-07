from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

# Create a password hasher using Argon2.
# This is a modern password hashing choice for new systems.
password_hash = PasswordHash.recommended()

# In the next improvement step, this secret should move into env settings.
SECRET_KEY = "change-this-in-phase-3-2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


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
    expires_at = utc_now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Returns the decoded payload if valid.
    Raises JWTError if the token is invalid, expired, or malformed.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
