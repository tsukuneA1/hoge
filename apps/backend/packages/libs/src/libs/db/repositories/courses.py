from libs.db.gen import courses, models
from sqlalchemy import Connection


class CoursesRepository:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.querier = courses.Querier(connection)

    def list(self, year: int) -> list[models.Course]:
        return self.querier.list_courses(year=year)

    def upsert(self, course: models.Course):
        self.querier.upsert_course(
            pkey=course.pkey,
            academic_year=course.academic_year,
            faculty=course.faculty,
            title=course.title,
            instructor=course.instructor,
            term_day_period=course.term_day_period,
            category=course.category,
            eligible_year=course.eligible_year,
            credits=course.credits,
            classroom=course.classroom,
            campus=course.campus,
            course_key=course.course_key,
            class_code=course.class_code,
            language=course.language,
            delivery_mode=course.delivery_mode,
            course_code=course.course_code,
            field_large=course.field_large,
            field_middle=course.field_middle,
            field_small=course.field_small,
            level=course.level,
            class_format=course.class_format,
            subtitle=course.subtitle,
            overview=course.overview,
            objectives=course.objectives,
            before_after_study=course.before_after_study,
            lesson_plan=course.lesson_plan,
            textbook=course.textbook,
            reference_text=course.reference_text,
            grading_policy=course.grading_policy,
            remarks=course.remarks,
            syllabus_updated_at=course.syllabus_updated_at,
            source_url=course.source_url,
            raw_html=course.raw_html,
        )
