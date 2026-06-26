class DomainError(Exception):
    """Base exception for domain errors."""


class CourseNotFoundError(DomainError):
    """Raised when a course is not found."""

    def __init__(self, pkey: str):
        self.pkey = pkey
        super().__init__(f"Course not found: {pkey}")
