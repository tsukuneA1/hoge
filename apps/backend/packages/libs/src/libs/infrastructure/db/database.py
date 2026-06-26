from collections.abc import Iterator
from contextlib import contextmanager
from logging import getLogger

import sqlalchemy

logger = getLogger(__name__)

_engine: sqlalchemy.Engine | None = None


def init_engine(
    database_url: str,
    *,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_pre_ping: bool = True,
    pool_recycle: int = 300,
) -> None:
    """Initialize the database engine at application startup.

    Args:
        database_url: SQLAlchemy database URL (postgresql+psycopg://...)
        pool_size: Number of persistent connections in the pool.
        max_overflow: Max extra connections beyond pool_size under load.
        pool_pre_ping: Validate connections before reuse to detect stale connections.
        pool_recycle: Recycle connections after this many seconds.
    """
    global _engine
    if _engine is not None:
        logger.warning(
            "Database engine already initialized; ignoring re-initialization"
        )
        return
    _engine = sqlalchemy.create_engine(
        database_url,
        echo=False,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=pool_pre_ping,
        pool_recycle=pool_recycle,
    )


def get_engine() -> sqlalchemy.Engine:
    """Get the database engine"""
    if _engine is None:
        raise RuntimeError("Database engine not initialized. Call init_engine() first.")
    return _engine


@contextmanager
def get_connection() -> Iterator[sqlalchemy.Connection]:
    """Get database connection context manager."""
    engine = get_engine()
    with engine.connect() as conn:
        yield conn


def close_engine() -> None:
    """Close the database engine."""
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None
