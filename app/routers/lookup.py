from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.lookups import Category, Religion, Caste
from app.schemas.lookup import (
    CategoryCreate, CategoryResponse,
    ReligionCreate, ReligionResponse,
    CasteCreate, CasteResponse
)

router = APIRouter(tags=["Lookups"])

# ─── Categories ───────────────────────────────────────────────────────
# NOTE: DELETE is intentionally removed — categories are FK-referenced in
# StudentDemographics. Deleting them would break existing student records.

@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    category = Category(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()

@router.patch("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.category_id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.category_name = data.category_name
    await db.commit()
    await db.refresh(category)
    return category

# ─── Religions ────────────────────────────────────────────────────────
# NOTE: DELETE is intentionally removed — religions are FK-referenced in
# StudentDemographics. Deleting them would break existing student records.

@router.post("/religions", response_model=ReligionResponse, status_code=201)
async def create_religion(data: ReligionCreate, db: AsyncSession = Depends(get_db)):
    religion = Religion(**data.model_dump())
    db.add(religion)
    await db.commit()
    await db.refresh(religion)
    return religion

@router.get("/religions", response_model=list[ReligionResponse])
async def get_religions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Religion))
    return result.scalars().all()

@router.patch("/religions/{religion_id}", response_model=ReligionResponse)
async def update_religion(religion_id: int, data: ReligionCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Religion).where(Religion.religion_id == religion_id))
    religion = result.scalar_one_or_none()
    if not religion:
        raise HTTPException(status_code=404, detail="Religion not found")
    religion.religion_name = data.religion_name
    await db.commit()
    await db.refresh(religion)
    return religion

# ─── Castes ───────────────────────────────────────────────────────────
# NOTE: DELETE is intentionally removed — castes are FK-referenced in
# StudentDemographics. Deleting them would break existing student records.

@router.post("/castes", response_model=CasteResponse, status_code=201)
async def create_caste(data: CasteCreate, db: AsyncSession = Depends(get_db)):
    caste = Caste(**data.model_dump())
    db.add(caste)
    await db.commit()
    await db.refresh(caste)
    return caste

@router.get("/castes", response_model=list[CasteResponse])
async def get_castes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Caste))
    return result.scalars().all()

@router.patch("/castes/{caste_id}", response_model=CasteResponse)
async def update_caste(caste_id: int, data: CasteCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Caste).where(Caste.caste_id == caste_id))
    caste = result.scalar_one_or_none()
    if not caste:
        raise HTTPException(status_code=404, detail="Caste not found")
    caste.caste_name = data.caste_name
    await db.commit()
    await db.refresh(caste)
    return caste