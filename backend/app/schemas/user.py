from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema used when registering a new user.
    """
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)

    # Keep strong minimum length.
    # We no longer need bcrypt's 72-byte restriction because Argon2 does not
    # have that same legacy limitation.
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """
    Schema used when logging in.
    """
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    """
    Schema returned to the client for user data.
    """
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    Schema returned after successful authentication.
    """
    access_token: str
    token_type: str = "bearer"
