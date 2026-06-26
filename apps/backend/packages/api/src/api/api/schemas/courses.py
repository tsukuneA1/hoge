from datetime import datetime

from pydantic import BaseModel


class CourseListItem(BaseModel):
    """Response model for course list (without values)."""

    pkey: str
    academic_year: int
    faculty: str
    title: str
    instructor: str
    term_day_period: str
    category: str | None
    eligible_year: str | None
    credits: int
    campus: str | None
    course_key: str | None
    class_code: str | None
    language: str | None
    delivery_mode: str | None
    field_large: str | None
    field_middle: str | None
    field_small: str | None
    level: str | None
    class_format: str | None


class CourseListResponse(BaseModel):
    """Response model for course list endpoint."""

    items: list[CourseListItem]
    total: int
    limit: int
    offset: int


class CourseResponse(CourseListItem):
    """Response model for course endpoint."""

    classroom: str | None
    course_code: str | None
    subtitle: str | None
    overview: str | None
    objectives: str | None
    before_after_study: str | None
    lesson_plan: str | None
    textbook: str | None
    reference_text: str | None
    grading_policy: str | None
    remarks: str | None
    syllabus_updated_at: datetime | None
    source_url: str
    created_at: datetime
    updated_at: datetime


class ErrorResponse(BaseModel):
    """Error response model for course API errors."""

    detail: str
