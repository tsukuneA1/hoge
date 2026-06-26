from typing import Annotated

from api.api.schemas.courses import (
    CourseListResponse,
    CourseResponse,
    ErrorResponse,
)
from api.services.course_service import CourseService
from api.services.dependencies import get_course_service
from api.services.exceptions import CourseNotFoundError
from fastapi import APIRouter, Depends, HTTPException, Query, status

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=CourseListResponse)
def list_courses(
    service: Annotated[CourseService, Depends(get_course_service)],
    academic_year: Annotated[int, Query(description="開講年度")],
    q: Annotated[str | None, Query(description="検索キーワード")] = None,
    faculty: Annotated[str | None, Query(description="対象学部")] = None,
    campus: Annotated[str | None, Query(description="対象キャンパス")] = None,
    language: Annotated[str | None, Query(description="言語")] = None,
    delivery_mode: Annotated[str | None, Query(description="授業方式")] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> CourseListResponse:
    return service.list_courses(
        academic_year=academic_year,
        q=q,
        faculty=faculty,
        campus=campus,
        language=language,
        delivery_mode=delivery_mode,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{pkey}",
    response_model=CourseResponse,
    responses={404: {"model": ErrorResponse, "description": "Course not found"}},
)
def get_course(
    pkey: str,
    course_service: Annotated[CourseService, Depends(get_course_service)],
) -> CourseResponse:
    try:
        course = course_service.get_course(pkey=pkey)
    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {pkey} not found"
        )

    return course
