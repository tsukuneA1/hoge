from collections.abc import Iterator

from libs.infrastructure.db.gen import courses, models
from sqlalchemy import Connection


class CoursesRepository:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.querier = courses.Querier(connection)

    def list(self) -> Iterator[models.Course]:
        return self.querier.list_courses()

    def upsert(self, course: courses.UpsertCoursesParams):
        self.querier.upsert_courses(course)
