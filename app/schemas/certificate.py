from typing import Optional
from pydantic import BaseModel

class CertificateCreate(BaseModel):
    certificate_type: str
    reason: Optional[str] = None
    academic_year: Optional[str] = None
    last_academic_year: Optional[str] = None
    last_year_result_copy: Optional[str] = None
    current_fee_receipt: Optional[str] = None
    last_fee_receipt: Optional[str] = None
    admission_proof: Optional[str] = None
    applicant_signature: Optional[str] = None

class CertificateUpdate(BaseModel):
    certificate_type: Optional[str] = None
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
    class Config:
        from_attributes = True