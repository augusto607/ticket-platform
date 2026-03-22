from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """
    Small endpoint to confirm the API is alive.
    Useful for debugging, testing, and container checks.
    """
    return {"status": "ok"}
