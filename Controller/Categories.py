# Controller/Categories.py
from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    title: str
    category_type: int


class CategoryCreate(CategoryBase):
    owner_id: int


class CategoryUpdate(BaseModel):
    title: Optional[str]
    category_type: Optional[int] = None


class CategoryInDB(CategoryBase):
    id: int
    owner_id: int

    class Config:
        orm_mode: True
