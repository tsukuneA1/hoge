from collections.abc import Iterator
from contextlib import contextmanager

import sqlalchemy
from libs.infrastructure.db import database as db

from api.config import settings


def init_engine() -> None:
    db.init_engine(
        settings.sqlalchemy_database_url, pool_size=settings.DB_SQLALCHEMY_POOL_SIZE
    )


def get_engine() -> sqlalchemy.Engine:
    return db.get_engine()


@contextmanager
def get_connection() -> Iterator[sqlalchemy.Connection]:
    with db.get_connection() as conn:
        yield conn


def close_engine() -> None:
    db.close_engine()
