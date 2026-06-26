from libs.infrastructure.db.repositories import courses
from libs.infrastructure.db.gen import models


class CourseService:
    def __init__(self, courses_repository: courses.CoursesRepository):
        self.course_repo = courses_repository

    async def get_course(self, pkey: str) -> models.Course:
        course = await self.course_repo.get_by_pkey(pkey=pkey)
        return course

    async def list_courses(self) -> list[models.Course]:
        return await self.course_repo.list(
            q=
        )
