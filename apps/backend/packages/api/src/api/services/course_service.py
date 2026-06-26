from libs.infrastructure.db.gen import models
from libs.infrastructure.db.repositories import courses

from api.api.schemas.courses import CourseListResponse


class CourseService:
    def __init__(self, courses_repository: courses.CoursesRepository):
        self.course_repo = courses_repository

    def get_course(self, pkey: str) -> models.Course:
        course = self.course_repo.get_by_pkey(pkey=pkey)
        if course is None:
            raise
        return course

    def list_courses(
        self,
        *,
        academic_year: int,
        q: str | None,
        faculty: str | None,
        campus: str | None,
        language: str | None,
        delivery_mode: str | None,
        limit: int,
        offset: int,
    ) -> CourseListResponse:
        items = self.course_repo.list(
            academic_year=academic_year,
            q=_normalize_optional_query(q),
            faculty=faculty,
            campus=campus,
            language=language,
            delivery_mode=delivery_mode,
            limit_count=limit,
            offset_count=offset,
        )
        total = self.course_repo.count_courses(
            academic_year=academic_year, q=_normalize_optional_query(q)
        )

        return CourseListResponse(items=items, total=total, limit=limit, offset=offset)


def _normalize_optional_query(value: str | None) -> str | None:
    if value is None:
        return None

    value = value.strip()
    if value == "":
        return None

    return value
