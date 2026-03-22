from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Create the SQLAlchemy engine
# The engine is the main entry point to the database connection.
engine = create_engine(settings.database_url)

# SessionLocal creates database sessions.
# Each request can use its own session safely.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class that all ORM models will inherit from
Base = declarative_base()


def get_db():
    """
    Dependency function used by FastAPI endpoints.

    It creates a DB session, yields it to the route,
    and closes it automatically after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
