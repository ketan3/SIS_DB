from typing import Optional
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    category_name: str

class CategoryResponse(CategoryCreate):
    category_id: int
    class Config:
        from_attributes = True

class ReligionCreate(BaseModel):
    religion_name: str

class ReligionResponse(ReligionCreate):
    religion_id: int
    class Config:
        from_attributes = True

class CasteCreate(BaseModel):
    caste_name: str
    religion_id: Optional[int] = None  # Scopes caste to a religion (Hindu/Muslim/etc.)

class CasteResponse(CasteCreate):
    caste_id: int
    class Config:
        from_attributes = True