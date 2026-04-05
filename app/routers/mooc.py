from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.mooc import MoocCourse, StudentMoocEnrollment
from app.schemas.mooc import (
    MoocCourseCreate, MoocCourseUpdate, MoocCourseResponse,
    MoocEnrollmentCreate, MoocEnrollmentUpdate, MoocEnrollmentResponse,
    MoocEnrollmentDetailResponse
)

router = APIRouter(tags=["MOOC"])

# ─── MOOC Courses ─────────────────────────────────────────────────────

@router.post("/mooc-courses", response_model=MoocCourseResponse, status_code=201)
async def create_mooc_course(data: MoocCourseCreate, db: AsyncSession = Depends(get_db)):
    course = MoocCourse(**data.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course

@router.get("/mooc-courses", response_model=list[MoocCourseResponse])
async def get_mooc_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MoocCourse))
    return result.scalars().all()

@router.get("/mooc-courses/{mooc_course_id}", response_model=MoocCourseResponse)
async def get_mooc_course(mooc_course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MoocCourse).where(MoocCourse.mooc_course_id == mooc_course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="MOOC course not found")
    return course

@router.patch("/mooc-courses/{mooc_course_id}", response_model=MoocCourseResponse)
async def update_mooc_course(mooc_course_id: int, data: MoocCourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MoocCourse).where(MoocCourse.mooc_course_id == mooc_course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="MOOC course not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course

@router.delete("/mooc-courses/{mooc_course_id}", status_code=204)
async def delete_mooc_course(mooc_course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MoocCourse).where(MoocCourse.mooc_course_id == mooc_course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="MOOC course not found")
    await db.delete(course)
    await db.commit()

# ─── Student MOOC Enrollments ─────────────────────────────────────────

@router.post("/students/{student_id}/mooc-enrollments", response_model=MoocEnrollmentResponse, status_code=201)
async def create_mooc_enrollment(student_id: int, data: MoocEnrollmentCreate, db: AsyncSession = Depends(get_db)):
    enrollment = StudentMoocEnrollment(student_id=student_id, **data.model_dump())
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

@router.get("/students/{student_id}/mooc-enrollments", response_model=list[MoocEnrollmentDetailResponse])
async def get_mooc_enrollments(student_id: int, db: AsyncSession = Depends(get_db)):
    """Returns all MOOC enrollments with full course details expanded (name, platform, credits etc.)"""
    result = await db.execute(
        select(StudentMoocEnrollment, MoocCourse)
        .join(MoocCourse, StudentMoocEnrollment.mooc_course_id == MoocCourse.mooc_course_id)
        .where(StudentMoocEnrollment.student_id == student_id)
    )
    rows = result.all()
    response = []
    for enrollment, course in rows:
        response.append(MoocEnrollmentDetailResponse(
            mooc_id=enrollment.mooc_id,
            student_id=enrollment.student_id,
            enrollment_id=enrollment.enrollment_id,
            grade=enrollment.grade,
            completion_date=enrollment.completion_date,
            certificate_url=enrollment.certificate_url,
            course=MoocCourseResponse.model_validate(course)
        ))
    return response

@router.patch("/students/{student_id}/mooc-enrollments/{mooc_id}", response_model=MoocEnrollmentResponse)
async def update_mooc_enrollment(student_id: int, mooc_id: int, data: MoocEnrollmentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentMoocEnrollment).where(
            StudentMoocEnrollment.mooc_id == mooc_id,
            StudentMoocEnrollment.student_id == student_id
        )
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="MOOC enrollment not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(enrollment, key, value)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

@router.delete("/students/{student_id}/mooc-enrollments/{mooc_id}", status_code=204)
async def delete_mooc_enrollment(student_id: int, mooc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudentMoocEnrollment).where(
            StudentMoocEnrollment.mooc_id == mooc_id,
            StudentMoocEnrollment.student_id == student_id
        )
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="MOOC enrollment not found")
    await db.delete(enrollment)
    await db.commit()