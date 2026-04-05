from datetime import date
from typing import Optional
from pydantic import BaseModel

class MoocCourseCreate(BaseModel):
    platform: str
    course_name: str
    provider_university: Optional[str] = None
    course_code: Optional[str] = None
    duration: Optional[str] = None
    total_hours: Optional[int] = None
    credit_points: Optional[int] = None

class MoocCourseUpdate(BaseModel):
    platform: Optional[str] = None
    course_name: Optional[str] = None
    provider_university: Optional[str] = None
    course_code: Optional[str] = None
    duration: Optional[str] = None
    total_hours: Optional[int] = None
    credit_points: Optional[int] = None

class MoocCourseResponse(MoocCourseCreate):
    mooc_course_id: int
    class Config:
        from_attributes = True

class MoocEnrollmentCreate(BaseModel):
    mooc_course_id: int
    enrollment_id: Optional[int] = None  # Links MOOC credit to a specific semester
    grade: Optional[str] = None
    completion_date: Optional[date] = None
    certificate_url: Optional[str] = None

class MoocEnrollmentUpdate(BaseModel):
    grade: Optional[str] = None
    completion_date: Optional[date] = None
    certificate_url: Optional[str] = None

class MoocEnrollmentResponse(MoocEnrollmentCreate):
    mooc_id: int
    student_id: int
    class Config:
        from_attributes = True


# Issue #9: Expanded response that includes full course details for frontend cards
class MoocEnrollmentDetailResponse(BaseModel):
    mooc_id: int
    student_id: int
    enrollment_id: Optional[int] = None
    grade: Optional[str] = None
    completion_date: Optional[date] = None
    certificate_url: Optional[str] = None
    course: MoocCourseResponse  # Full course detail embedded

    class Config:
        from_attributes = True