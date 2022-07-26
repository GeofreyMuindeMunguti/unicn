from typing import Generator

from app.db.session import get_session, get_engine
from sqlalchemy.engine import Engine
from fastapi import Depends


def get_db(engine: Engine = Depends(get_engine)) -> Generator:
    with get_session(engine=engine) as db:
        yield db
