from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.academic import EnrollmentMapping
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse

router = APIRouter(prefix="/enrollments", tags=["Enrollment Mapping"])

@router.post("/", response_model=EnrollmentResponse, status_code=201)
async def create_enrollment(data: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    enrollment = EnrollmentMapping(**data.model_dump())
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

@router.get("/", response_model=list[EnrollmentResponse])
async def get_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EnrollmentMapping))
    return result.scalars().all()

# NOTE: This route MUST come before /{enrollment_id} — otherwise FastAPI
# tries to cast the literal "student" as an int and returns a 422 error.
@router.get("/student/{student_id}", response_model=list[EnrollmentResponse])
async def get_enrollments_by_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EnrollmentMapping).where(EnrollmentMapping.student_id == student_id)
    )
    return result.scalars().all()

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EnrollmentMapping).where(EnrollmentMapping.enrollment_id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@router.patch("/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(enrollment_id: int, data: EnrollmentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EnrollmentMapping).where(EnrollmentMapping.enrollment_id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(enrollment, key, value)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

@router.delete("/{enrollment_id}", status_code=204)
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EnrollmentMapping).where(EnrollmentMapping.enrollment_id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    await db.delete(enrollment)
    await db.commit()