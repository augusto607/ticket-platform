from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.tickets import router as tickets_router
from app.core.config import settings
from app.core.db import Base, engine
from app.models.ticket import Ticket  # noqa: F401

# Create database tables at startup time.
# IMPORTANT:
# This is acceptable for Phase 1 learning.
# In a more production-like setup, we will replace this with Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Portfolio-grade ticket management backend built with FastAPI.",
)

app.include_router(health_router)
app.include_router(tickets_router)


@app.get("/")
def root():
    return {
        "message": "Ticket Platform API is running",
        "environment": settings.app_env,
    }
