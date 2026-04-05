from typing import Optional
from pydantic import BaseModel

class AddressCreate(BaseModel):
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    country: str

class AddressResponse(AddressCreate):
    address_id: int
    class Config:
        from_attributes = True

class StudentAddressCreate(BaseModel):
    address_id: int
    address_type: str  # permanent, current, guardian

class StudentAddressResponse(StudentAddressCreate):
    student_address_id: int
    student_id: int
    class Config:
        from_attributes = True