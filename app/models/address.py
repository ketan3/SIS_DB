from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class Address(Base):
    __tablename__ = 'addresses'
    
    address_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    line1: Mapped[str] = mapped_column(String(100), nullable=False)
    line2: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    pincode: Mapped[str] = mapped_column(String(10), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)

class StudentAddress(Base):
    __tablename__ = 'student_addresses'
    
    student_address_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('student_information.student_id'), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.address_id'), nullable=False)
    address_type: Mapped[str] = mapped_column(String(20), nullable=False)
    
    __table_args__ = (
        CheckConstraint(
            "address_type IN ('permanent', 'current', 'guardian')", 
            name='chk_address_type'
        ),
    )
