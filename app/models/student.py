from datetime import date
from sqlalchemy import Column, String, Integer, Date, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class StudentInformation(Base):
    __tablename__ = 'student_information'
    
    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    
    mobile_number: Mapped[str | None] = mapped_column(String(15), unique=True)
    email_id: Mapped[str | None] = mapped_column(String(100), unique=True)
    blood_group: Mapped[str] = mapped_column(String(5), nullable=False)
    
    roll_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    abc_id: Mapped[str | None] = mapped_column(String(20), unique=True)
    eligibility_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    prn_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    
    admission_date: Mapped[date | None] = mapped_column(Date)

    # Status flag — use soft-delete instead of hard DELETE
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, server_default="true")

    # Financial fields
    total_academic_fee: Mapped[float | None] = mapped_column(Numeric(10, 2))
    total_submitted_fee: Mapped[int | None] = mapped_column(Integer)
    total_pending_fee: Mapped[int | None] = mapped_column(Integer)
    scholarship_applied: Mapped[bool | None] = mapped_column(Boolean)
    scholarship_amount: Mapped[float | None] = mapped_column(Numeric(10, 2))
    
    # Class and Documents
    apply_for_class: Mapped[str | None] = mapped_column(String(50))
    student_photo: Mapped[str | None] = mapped_column(String(255))
    applicant_signature: Mapped[str | None] = mapped_column(String(255))
    last_qualifying_exam: Mapped[str | None] = mapped_column(String(100))
    last_exam_seat_number: Mapped[str | None] = mapped_column(String(20))
    last_exam_board: Mapped[str | None] = mapped_column(String(100))

class StudentDemographics(Base):
    __tablename__ = 'student_demographics'
    
    student_id: Mapped[int] = mapped_column(ForeignKey('student_information.student_id'), primary_key=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey('categories.category_id'))
    religion_id: Mapped[int | None] = mapped_column(ForeignKey('religions.religion_id'))
    caste_id: Mapped[int | None] = mapped_column(ForeignKey('castes.caste_id'))

class StudentFamilyDetails(Base):
    __tablename__ = 'student_family_details'
    
    family_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('student_information.student_id'), nullable=False)
    
    parent1_name: Mapped[str | None] = mapped_column(String(100))
    parent1_phone: Mapped[str | None] = mapped_column(String(15))
    parent1_occupation: Mapped[str | None] = mapped_column(String(100))
    parent1_photo: Mapped[str | None] = mapped_column(String(255))
    
    parent2_name: Mapped[str | None] = mapped_column(String(100))
    parent2_phone: Mapped[str | None] = mapped_column(String(15))
    parent2_occupation: Mapped[str | None] = mapped_column(String(100))
    
    guardian_type: Mapped[str | None] = mapped_column(String(50))
    guardian_name: Mapped[str | None] = mapped_column(String(100))
    guardian_phone: Mapped[str | None] = mapped_column(String(15))
    guardian_occupation: Mapped[str | None] = mapped_column(String(100))
