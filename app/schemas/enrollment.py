from typing import Optional
from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    student_id: int
    # String names removed — use department_id/class_id (external module FKs).
    # Storing both string + ID creates sync drift risk.
    department_id: Optional[int] = None  # FK to Department module
    program: Optional[str] = None
    class_id: Optional[int] = None       # FK to Class module
    division: Optional[str] = None
    batch: Optional[str] = None
    placement_id: Optional[int] = None   # FK to Placement module
    academic_id: Optional[int] = None    # FK to Academic Year module

class EnrollmentUpdate(BaseModel):
    department_id: Optional[int] = None
    program: Optional[str] = None
    class_id: Optional[int] = None
    division: Optional[str] = None
    batch: Optional[str] = None
    placement_id: Optional[int] = None
    academic_id: Optional[int] = None

class EnrollmentResponse(EnrollmentCreate):
    enrollment_id: int
    class Config:
        from_attributes = True