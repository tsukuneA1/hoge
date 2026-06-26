from typing import Annotated

from api.services.dependencies import get_course_service
from api.services.exceptions import CourseNotFoundError
from fastapi import APIRouter, Depends, HTTPException, status

from api.api.schemas.courses import (
    ErrorResponse,
    CourseListItem,
    CourseListResponse,
    CourseResponse
)

from api.services.course_service import CourseService

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.get("", response_model=CourseListResponse)
async def list_courses(
    "/{}"
) -> CourseListResponse:
    courses = await 

@router.get(
    "/{pkey}",
    response_model=CourseResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Course not found"}
    },
)
async def get_course(
    pkey: str,
    course_service: Annotated[CourseService, Depends(get_course_service)],
) -> CourseResponse:
    try:
        course = await course_service.get_course(pkey=pkey)
    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course {pkey} not found"
        )

    return CourseResponse(
        
    )

