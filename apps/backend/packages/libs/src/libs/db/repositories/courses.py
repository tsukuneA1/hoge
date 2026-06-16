from libs.db.gen import courses, models
from sqlalchemy import Connection


class CoursesRepository:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.querier = courses.Querier(connection)

    def list(self, year: int) -> list[models.Course]:
        return self.querier.list_courses()

    def upsert(self, course: models.Course):
        self.querier.upsert_course()
