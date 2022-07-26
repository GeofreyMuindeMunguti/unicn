from __future__ import with_statement

import logging
import os
import time
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, text

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from sqlalchemy.exc import OperationalError
from tabulate import tabulate

from alembic import context

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

from app.db.base import Base  # noqa

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

logger = logging.getLogger("alembic")


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql://{user}:{password}@{server}/{db}"


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            connect_args={
                "application_name": "alembic",
                "options": "-c lock_timeout=60000",  # In milliseconds
            },
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        max_runs = 3
        counter = 0
        while True:
            try:
                with context.begin_transaction():
                    context.run_migrations()
                break
            except OperationalError as e:
                if "DeadlockDetected" in str(e) or "LockNotAvailable" in str(e):
                    logger.info("A deadlock/lock timeout has occurred.")
                    logger.info(
                        "Waiting for 60s before attempting the migrations again."
                    )
                    time.sleep(60)
                    counter += 1
                    if counter >= max_runs:
                        logger.info("Unable to acquire locks, raising deadlock error.")
                        raise
                else:
                    raise
            except Exception as e:
                logger.error(e)
                raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
