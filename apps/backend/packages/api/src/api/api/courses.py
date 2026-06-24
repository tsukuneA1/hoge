from fastapi import APIRouter, Depends, HTTPException, status

from api.api.schemas.courses import (
    ErrorResponse,
    CourseListItem,
    CourseListResponse,
    CourseResponse
)

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.get("", response_model=CourseListResponse)
async def list_courses(

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
) -> CourseResponse:
    try
