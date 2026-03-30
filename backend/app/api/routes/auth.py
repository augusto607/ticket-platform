from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Flow:
    1. Check if email is already in use
    2. Hash the password
    3. Create the user
    4. Return safe user data (never the password hash)
    """
    repository = UserRepository(db)

    existing_user = repository.get_by_email(user_data.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    hashed_password = hash_password(user_data.password)

    created_user = repository.create(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
    )

    return created_user


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.

    Flow:
    1. Find the user by email
    2. Verify the password against the stored hash
    3. Return a signed access token
    """
    repository = UserRepository(db)

    user = repository.get_by_email(credentials.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user account is inactive.",
        )

    access_token = create_access_token(subject=user.email)

    return TokenResponse(access_token=access_token)
