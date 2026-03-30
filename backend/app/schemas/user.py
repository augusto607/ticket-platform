from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema used when registering a new user.
    """
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    # password: str = Field(..., min_length=8, max_length=128)
    password: str = Field(..., min_length=8, max_length=72)


class UserLogin(BaseModel):
    """
    Schema used when logging in.
    """
    email: EmailStr
    # password: str = Field(..., min_length=8, max_length=128)
    password: str = Field(..., min_length=8, max_length=72)


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
