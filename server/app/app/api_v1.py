from fastapi import APIRouter, Depends
from pydantic.annotated_types import Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core import deps

from app.auth.api import router as auth_router
from app.users.api import router as user_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, tags=["Authorization"])
api_router.include_router(user_router, tags=["users"])


@api_router.get("/health")
def get_api_status(db: Session = Depends(deps.get_db)) -> Any:
    db.execute(text("SELECT 1;"))
    return dict(status="Ok")
