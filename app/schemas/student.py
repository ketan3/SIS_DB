from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


# ─── StudentInformation ───────────────────────────────────────────────

class StudentCreate(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    date_of_birth: date
    gender: str
    blood_group: str

    mobile_number: Optional[str] = None
    email_id: Optional[str] = None

    roll_number: Optional[str] = None
    abc_id: Optional[str] = None
    eligibility_number: Optional[str] = None
    prn_number: Optional[str] = None

    admission_date: Optional[date] = None

    total_academic_fee: Optional[float] = None
    total_submitted_fee: Optional[int] = None
    total_pending_fee: Optional[int] = None
    scholarship_applied: Optional[bool] = None
    scholarship_amount: Optional[float] = None

    apply_for_class: Optional[str] = None
    student_photo: Optional[str] = None
    applicant_signature: Optional[str] = None
    last_qualifying_exam: Optional[str] = None
    last_exam_seat_number: Optional[str] = None
    last_exam_board: Optional[str] = None


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    mobile_number: Optional[str] = None
    email_id: Optional[str] = None
    roll_number: Optional[str] = None
    abc_id: Optional[str] = None
    eligibility_number: Optional[str] = None
    prn_number: Optional[str] = None
    admission_date: Optional[date] = None
    total_academic_fee: Optional[float] = None
    total_submitted_fee: Optional[int] = None
    total_pending_fee: Optional[int] = None
    scholarship_applied: Optional[bool] = None
    scholarship_amount: Optional[float] = None
    apply_for_class: Optional[str] = None
    student_photo: Optional[str] = None
    applicant_signature: Optional[str] = None
    last_qualifying_exam: Optional[str] = None
    last_exam_seat_number: Optional[str] = None
    last_exam_board: Optional[str] = None


class StudentResponse(StudentCreate):
    student_id: int

    class Config:
        from_attributes = True


# ─── StudentDemographics ──────────────────────────────────────────────

class DemographicsCreate(BaseModel):
    category_id: Optional[int] = None
    religion_id: Optional[int] = None
    caste_id: Optional[int] = None


class DemographicsResponse(DemographicsCreate):
    student_id: int

    class Config:
        from_attributes = True


# ─── StudentFamilyDetails ─────────────────────────────────────────────

class FamilyCreate(BaseModel):
    parent1_name: Optional[str] = None
    parent1_phone: Optional[str] = None
    parent1_occupation: Optional[str] = None
    parent1_photo: Optional[str] = None

    parent2_name: Optional[str] = None
    parent2_phone: Optional[str] = None
    parent2_occupation: Optional[str] = None

    guardian_type: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_occupation: Optional[str] = None


class FamilyResponse(FamilyCreate):
    family_id: int
    student_id: int

    class Config:
        from_attributes = True