from fastapi import APIRouter, Depends
from pydantic.annotated_types import Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core import deps

api_router = APIRouter()


@api_router.get("/health")
def get_api_status(db: Session = Depends(deps.get_db)) -> Any:
    db.execute(text("SELECT 1;"))
    return dict(status="Ok")
