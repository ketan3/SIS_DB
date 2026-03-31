from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class EnrollmentMapping(Base):
    __tablename__ = 'enrollment_mapping'
    
    enrollment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('student_information.student_id'), nullable=False)
    
    department: Mapped[str | None] = mapped_column(String(100))
    department_id: Mapped[int | None] = mapped_column(Integer) # External link
    program: Mapped[str | None] = mapped_column(String(100))
    class_name: Mapped[str | None] = mapped_column(String(50), name='class')
    class_id: Mapped[int | None] = mapped_column(Integer) # External link
    division: Mapped[str | None] = mapped_column(String(20))
    batch: Mapped[str | None] = mapped_column(String(20))
    placement_id: Mapped[int | None] = mapped_column(Integer) # External link
    academic_id: Mapped[int | None] = mapped_column(Integer) # External link

class CertificateRequest(Base):
    __tablename__ = 'certificate_request'
    
    request_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('student_information.student_id'), nullable=False)
    
    certificate_type: Mapped[str] = mapped_column(String(100), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    academic_year: Mapped[str | None] = mapped_column(String(20))
    last_academic_year: Mapped[str | None] = mapped_column(String(20))
    last_year_result_copy: Mapped[str | None] = mapped_column(String(255))
    current_fee_receipt: Mapped[str | None] = mapped_column(String(255))
    last_fee_receipt: Mapped[str | None] = mapped_column(String(255))
    admission_proof: Mapped[str | None] = mapped_column(String(255))
    applicant_signature: Mapped[str | None] = mapped_column(String(255))
