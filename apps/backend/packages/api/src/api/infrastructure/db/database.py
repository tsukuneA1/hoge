from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from api.config import settings
from libs.infrastructure.db import database as db


def init_engine() -> None:
    db.init_engine(
        settings.sqlalchemy_database_url, pool_size=settings.DB_SQLALCHEMY_POOL_SIZE
    )


def get_engine() -> AsyncEngine:
    return db.get_engine()


@asynccontextmanager
async def get_connection() -> AsyncIterator[AsyncConnection]:
    async with db.get_connection() as conn:
        yield conn


async def close_engine() -> None:
    await db.close_engine()
