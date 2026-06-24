from pydantic import BaseModel


class CourseListItem(BaseModel):
    """Response model for course list (without values)."""

    pkey: str


class CourseListResponse(BaseModel):
    """Response model for course list endpoint."""

    courses: list[CourseListItem]


class CourseResponse(BaseModel):
    """Response model for course endpoint."""


class ErrorResponse(BaseModel):
    """Error response model for course API errors."""

    detail: str
