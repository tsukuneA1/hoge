from collections.abc import Generator
from typing import Annotated

import sqlalchemy
from fastapi import Depends
from libs.infrastructure.db.repositories.courses import CoursesRepository

from api.infrastructure.db.database import get_connection
from api.services.course_service import CourseService


def get_db_connection() -> Generator[sqlalchemy.Connection]:
    with get_connection() as conn:
        yield conn


def get_course_service(
    conn: Annotated[sqlalchemy.Connection, Depends(get_db_connection)],
) -> CourseService:
    return CourseService(
        CoursesRepository(conn),
    )
