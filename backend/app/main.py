from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.tickets import router as tickets_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Portfolio-grade ticket management backend built with FastAPI.",
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tickets_router)


@app.get("/")
def root():
    """
    Root endpoint used as a quick sanity check.
    """
    return {
        "message": "Ticket Platform API is running",
        "environment": settings.app_env,
    }
