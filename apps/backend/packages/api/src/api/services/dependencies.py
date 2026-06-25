from collections.abc import AsyncGenerator
from typing import Annotated

from api.services.course_service import CourseService
from fastapi import Depends
from libs.infrastructure.db.repositories.courses import CoursesRepository

from sqlalchemy.ext.asyncio import AsyncConnection

from api.infrastructure.db.database import get_connection

async def get_db_connection() -> AsyncGenerator[AsyncConnection]:
    async with get_connection() as conn:
        yield conn

def get_course_service(
        conn: Annotated[AsyncConnection, Depends(get_db_connection)]
) -> CourseService:
    return CourseService(
        CoursesRepository(conn),
    )