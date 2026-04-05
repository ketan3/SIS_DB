from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.student import StudentInformation


async def get_student_or_404(student_id: int, db: AsyncSession) -> StudentInformation:
    """Reusable guard — raises 404 if the student doesn't exist or is deactivated."""
    result = await db.execute(
        select(StudentInformation).where(
            StudentInformation.student_id == student_id,
            StudentInformation.is_active == True
        )
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found or is inactive")
    return student
