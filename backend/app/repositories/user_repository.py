from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository responsible for direct user database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """
        Return one user by email, or None if not found.
        """
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, full_name: str, hashed_password: str) -> User:
        """
        Create and persist a new user.
        """
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
