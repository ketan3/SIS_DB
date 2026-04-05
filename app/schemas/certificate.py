from typing import Optional
from pydantic import BaseModel, Field

class CertificateCreate(BaseModel):
    certificate_type: str
    reason: Optional[str] = None
    academic_year: Optional[str] = None
    last_academic_year: Optional[str] = None
    # Document fields — store relative file paths (e.g. /uploads/docs/result.pdf)
    last_year_result_copy: Optional[str] = Field(default=None, description="Relative path to uploaded file, e.g. /uploads/docs/result.pdf")
    current_fee_receipt: Optional[str] = Field(default=None, description="Relative path to uploaded file")
    last_fee_receipt: Optional[str] = Field(default=None, description="Relative path to uploaded file")
    admission_proof: Optional[str] = Field(default=None, description="Relative path to uploaded file")
    applicant_signature: Optional[str] = Field(default=None, description="Relative path to uploaded signature image")

class CertificateUpdate(BaseModel):
    certificate_type: Optional[str] = None
    status: Optional[str] = None  # pending | approved | rejected | dispatched
    reason: Optional[str] = None
    academic_year: Optional[str] = None
    last_academic_year: Optional[str] = None
    last_year_result_copy: Optional[str] = None
    current_fee_receipt: Optional[str] = None
    last_fee_receipt: Optional[str] = None
    admission_proof: Optional[str] = None
    applicant_signature: Optional[str] = None

class CertificateResponse(CertificateCreate):
    request_id: int
    student_id: int
    status: str = 'pending'

    class Config:
        from_attributes = True