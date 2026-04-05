from typing import Optional
from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    student_id: int
    department: Optional[str] = None
    department_id: Optional[int] = None
    program: Optional[str] = None
    class_name: Optional[str] = None
    class_id: Optional[int] = None
    division: Optional[str] = None
    batch: Optional[str] = None
    placement_id: Optional[int] = None
    academic_id: Optional[int] = None

class EnrollmentUpdate(BaseModel):
    department: Optional[str] = None
    department_id: Optional[int] = None
    program: Optional[str] = None
    class_name: Optional[str] = None
    class_id: Optional[int] = None
    division: Optional[str] = None
    batch: Optional[str] = None
    placement_id: Optional[int] = None
    academic_id: Optional[int] = None

class EnrollmentResponse(EnrollmentCreate):
    enrollment_id: int
    class Config:
        from_attributes = True