from typing import ContextManager, Optional

from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import get_app_settings


def get_engine() -> Engine:
    settings = get_app_settings()

    def debug_mode() -> bool:
        return settings.APP_ENVIRONMENT == "debug"

    return create_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        future=True,
        echo=debug_mode(),
        pool_pre_ping=True,
        pool_size=1000,
        max_overflow=500,
        connect_args={
            "application_name": "app",
            "options": "-c statement_timeout=10000 -c idle_in_transaction_session_timeout=60000",
        },
    )


def get_session(engine: Optional[Engine] = None) -> ContextManager[Session]:
    if not engine:
        engine = get_engine()

    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True,
    )
    Session_ = scoped_session(session_factory)
    return Session_()
