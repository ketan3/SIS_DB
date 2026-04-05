from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.academic import CertificateRequest
from app.schemas.certificate import CertificateCreate, CertificateUpdate, CertificateResponse

router = APIRouter(tags=["Certificate Requests"])

@router.post("/students/{student_id}/certificates", response_model=CertificateResponse, status_code=201)
async def create_certificate_request(student_id: int, data: CertificateCreate, db: AsyncSession = Depends(get_db)):
    certificate = CertificateRequest(student_id=student_id, **data.model_dump())
    db.add(certificate)
    await db.commit()
    await db.refresh(certificate)
    return certificate

@router.get("/students/{student_id}/certificates", response_model=list[CertificateResponse])
async def get_certificate_requests(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CertificateRequest).where(CertificateRequest.student_id == student_id)
    )
    return result.scalars().all()

@router.get("/students/{student_id}/certificates/{request_id}", response_model=CertificateResponse)
async def get_certificate_request(student_id: int, request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CertificateRequest).where(
            CertificateRequest.request_id == request_id,
            CertificateRequest.student_id == student_id
        )
    )
    certificate = result.scalar_one_or_none()
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate request not found")
    return certificate

@router.patch("/students/{student_id}/certificates/{request_id}", response_model=CertificateResponse)
async def update_certificate_request(student_id: int, request_id: int, data: CertificateUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CertificateRequest).where(
            CertificateRequest.request_id == request_id,
            CertificateRequest.student_id == student_id
        )
    )
    certificate = result.scalar_one_or_none()
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate request not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(certificate, key, value)
    await db.commit()
    await db.refresh(certificate)
    return certificate

@router.delete("/students/{student_id}/certificates/{request_id}", status_code=204)
async def delete_certificate_request(student_id: int, request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CertificateRequest).where(
            CertificateRequest.request_id == request_id,
            CertificateRequest.student_id == student_id
        )
    )
    certificate = result.scalar_one_or_none()
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate request not found")
    await db.delete(certificate)
    await db.commit()