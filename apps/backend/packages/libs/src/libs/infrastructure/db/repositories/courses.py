from libs.infrastructure.db.gen import courses, models
from sqlalchemy import Connection


class CoursesRepository:
    def __init__(self, connection: Connection):
        self.querier = courses.Querier(connection)

    def list(self) -> list[models.Course]:
        return list(self.querier.list_courses())

    def upsert(self, course: courses.UpsertCoursesParams) -> None:
        self.querier.upsert_courses(course)
