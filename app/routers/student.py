from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.student import StudentInformation, StudentDemographics, StudentFamilyDetails
from app.schemas.student import (
    StudentCreate, StudentUpdate, StudentResponse,
    DemographicsCreate, DemographicsUpdate, DemographicsResponse,
    FamilyCreate, FamilyResponse
)

router = APIRouter(prefix="/students", tags=["Student Profile"])


# ─── StudentInformation CRUD ──────────────────────────────────────────

@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    student = StudentInformation(**data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


@router.get("/", response_model=list[StudentResponse])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StudentInformation))
    return result.scalars().all()


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentInformation).where(StudentInformation.student_id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.patch("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentInformation).where(StudentInformation.student_id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=200)
async def deactivate_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Soft-delete: marks student as inactive instead of permanently removing them."""
    result = await db.execute(
        select(StudentInformation).where(StudentInformation.student_id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.is_active = False
    await db.commit()
    return {"detail": f"Student {student_id} has been deactivated."}


# ─── StudentDemographics CRUD ─────────────────────────────────────────

@router.post("/{student_id}/demographics", response_model=DemographicsResponse, status_code=201)
async def create_demographics(student_id: int, data: DemographicsCreate, db: AsyncSession = Depends(get_db)):
    demographics = StudentDemographics(student_id=student_id, **data.model_dump())
    db.add(demographics)
    await db.commit()
    await db.refresh(demographics)
    return demographics


@router.get("/{student_id}/demographics", response_model=DemographicsResponse)
async def get_demographics(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentDemographics).where(StudentDemographics.student_id == student_id)
    )
    demo = result.scalar_one_or_none()
    if not demo:
        raise HTTPException(status_code=404, detail="Demographics not found")
    return demo


@router.patch("/{student_id}/demographics", response_model=DemographicsResponse)
async def update_demographics(student_id: int, data: DemographicsUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentDemographics).where(StudentDemographics.student_id == student_id)
    )
    demo = result.scalar_one_or_none()
    if not demo:
        raise HTTPException(status_code=404, detail="Demographics not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(demo, key, value)
    await db.commit()
    await db.refresh(demo)
    return demo


# ─── StudentFamilyDetails CRUD ────────────────────────────────────────

@router.post("/{student_id}/family", response_model=FamilyResponse, status_code=201)
async def create_family(student_id: int, data: FamilyCreate, db: AsyncSession = Depends(get_db)):
    family = StudentFamilyDetails(student_id=student_id, **data.model_dump())
    db.add(family)
    await db.commit()
    await db.refresh(family)
    return family


@router.get("/{student_id}/family", response_model=list[FamilyResponse])
async def get_family(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentFamilyDetails).where(StudentFamilyDetails.student_id == student_id)
    )
    return result.scalars().all()


@router.patch("/{student_id}/family/{family_id}", response_model=FamilyResponse)
async def update_family(student_id: int, family_id: int, data: FamilyCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentFamilyDetails).where(
            StudentFamilyDetails.family_id == family_id,
            StudentFamilyDetails.student_id == student_id
        )
    )
    family = result.scalar_one_or_none()
    if not family:
        raise HTTPException(status_code=404, detail="Family record not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(family, key, value)
    await db.commit()
    await db.refresh(family)
    return family


@router.delete("/{student_id}/family/{family_id}", status_code=204)
async def delete_family(student_id: int, family_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentFamilyDetails).where(
            StudentFamilyDetails.family_id == family_id,
            StudentFamilyDetails.student_id == student_id
        )
    )
    family = result.scalar_one_or_none()
    if not family:
        raise HTTPException(status_code=404, detail="Family record not found")
    await db.delete(family)
    await db.commit()