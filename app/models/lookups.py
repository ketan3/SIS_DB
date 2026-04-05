from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Category(Base):
    __tablename__ = 'categories'
    
    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class Religion(Base):
    __tablename__ = 'religions'
    
    religion_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    religion_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class Caste(Base):
    __tablename__ = 'castes'
    
    caste_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    caste_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # A caste belongs to a religion — Hindu castes differ from Muslim castes etc.
    religion_id: Mapped[int | None] = mapped_column(ForeignKey('religions.religion_id'), nullable=True)
