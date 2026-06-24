from datetime import datetime

from libs.infrastructure.db.gen import courses, models
from sqlalchemy import Connection


class CoursesRepository:
    def __init__(self, connection: Connection):
        self.querier = courses.Querier(connection)

    async def get_by_pkey(self, pkey: str) -> models.Course:
        return await self.querier.get_course_by_pkey(pkey=pkey)

    def list(self) -> list[models.Course]:
        return list(self.querier.list_courses())

    def upsert(
        self,
        pkey: str,
        academic_year: int,
        faculty: str,
        title: str,
        instructor: str,
        term_day_period: str,
        category: str,
        eligible_year: str,
        credits: int,
        classroom: str,
        campus: str,
        course_key: str,
        class_code: str,
        language: str,
        delivery_mode: str,
        course_code: str,
        field_large: str,
        field_middle: str,
        field_small: str,
        level: str,
        class_format: str,
        subtitle: str | None,
        overview: str,
        objectives: str,
        before_after_study: str,
        lesson_plan: str,
        textbook: str | None,
        reference_text: str | None,
        grading_policy: str,
        remarks: str,
        source_url: str,
        syllabus_updated_at: datetime,
        raw_html: str | None,
    ) -> None:
        params = courses.UpsertCoursesParams(
            pkey=pkey,
            academic_year=academic_year,
            faculty=faculty,
            title=title,
            instructor=instructor,
            term_day_period=term_day_period,
            category=category,
            eligible_year=eligible_year,
            credits=credits,
            classroom=classroom,
            campus=campus,
            course_key=course_key,
            class_code=class_code,
            language=language,
            delivery_mode=delivery_mode,
            course_code=course_code,
            field_large=field_large,
            field_middle=field_middle,
            field_small=field_small,
            level=level,
            class_format=class_format,
            subtitle=subtitle,
            overview=overview,
            objectives=objectives,
            before_after_study=before_after_study,
            lesson_plan=lesson_plan,
            textbook=textbook,
            reference_text=reference_text,
            grading_policy=grading_policy,
            remarks=remarks,
            source_url=source_url,
            syllabus_updated_at=syllabus_updated_at,
            raw_html=raw_html,
        )
        self.querier.upsert_courses(params)
