from fastapi import APIRouter, Request
from sqlalchemy import text
from app.db.database import engine

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("")
def health(request: Request):
    try:
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
        return {"status": "running", "database": "ok"}
    except Exception as e:
        return {"status": "running", "database": "error", "detail": e.__class__.__name__}
