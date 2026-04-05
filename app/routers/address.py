from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.address import Address, StudentAddress
from app.schemas.address import (
    AddressCreate, AddressResponse,
    StudentAddressCreate, StudentAddressResponse
)

router = APIRouter(tags=["Addresses"])

# ─── Address ──────────────────────────────────────────────────────────
# NOTE: GET /addresses and DELETE /addresses/{id} are intentionally removed.
# Addresses are only meaningful in the context of a student.
# Use POST to create an address record, then link it via StudentAddress.

@router.post("/addresses", response_model=AddressResponse, status_code=201)
async def create_address(data: AddressCreate, db: AsyncSession = Depends(get_db)):
    address = Address(**data.model_dump())
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address

@router.patch("/addresses/{address_id}", response_model=AddressResponse)
async def update_address(address_id: int, data: AddressCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Address).where(Address.address_id == address_id))
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(address, key, value)
    await db.commit()
    await db.refresh(address)
    return address

# ─── StudentAddress CRUD ──────────────────────────────────────────────

@router.post("/students/{student_id}/addresses", response_model=StudentAddressResponse, status_code=201)
async def create_student_address(student_id: int, data: StudentAddressCreate, db: AsyncSession = Depends(get_db)):
    student_address = StudentAddress(student_id=student_id, **data.model_dump())
    db.add(student_address)
    await db.commit()
    await db.refresh(student_address)
    return student_address

@router.get("/students/{student_id}/addresses", response_model=list[StudentAddressResponse])
async def get_student_addresses(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentAddress).where(StudentAddress.student_id == student_id)
    )
    return result.scalars().all()

@router.patch("/students/{student_id}/addresses/{student_address_id}", response_model=StudentAddressResponse)
async def update_student_address(student_id: int, student_address_id: int, data: StudentAddressCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentAddress).where(
            StudentAddress.student_address_id == student_address_id,
            StudentAddress.student_id == student_id
        )
    )
    student_address = result.scalar_one_or_none()
    if not student_address:
        raise HTTPException(status_code=404, detail="Student address not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student_address, key, value)
    await db.commit()
    await db.refresh(student_address)
    return student_address

@router.delete("/students/{student_id}/addresses/{student_address_id}", status_code=204)
async def delete_student_address(student_id: int, student_address_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentAddress).where(
            StudentAddress.student_address_id == student_address_id,
            StudentAddress.student_id == student_id
        )
    )
    student_address = result.scalar_one_or_none()
    if not student_address:
        raise HTTPException(status_code=404, detail="Student address not found")
    await db.delete(student_address)
    await db.commit()