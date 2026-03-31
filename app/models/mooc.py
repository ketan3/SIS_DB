from datetime import date
from sqlalchemy import String, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class MoocCourse(Base):
    __tablename__ = 'mooc_courses'
    
    mooc_course_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_university: Mapped[str | None] = mapped_column(String(150))
    course_code: Mapped[str | None] = mapped_column(String(50))
    course_name: Mapped[str] = mapped_column(String(200), nullable=False)
    duration: Mapped[str | None] = mapped_column(String(50))
    total_hours: Mapped[int | None] = mapped_column(Integer)
    credit_points: Mapped[int | None] = mapped_column(Integer)
    
    __table_args__ = (
        UniqueConstraint('course_code', 'platform', name='unique_course_platform'),
    )

class StudentMoocEnrollment(Base):
    __tablename__ = 'student_mooc_enrollments'
    
    mooc_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('student_information.student_id'), nullable=False)
    mooc_course_id: Mapped[int] = mapped_column(ForeignKey('mooc_courses.mooc_course_id'), nullable=False)
    
    grade: Mapped[str | None] = mapped_column(String(10))
    completion_date: Mapped[date | None] = mapped_column(Date)
    certificate_url: Mapped[str | None] = mapped_column(String(255))
