# Controller/Categories.py
from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    title: str
    color: Optional[str]
    category_type: int


class CategoryCreate(CategoryBase):
    owner_id: int

class CategoryUpdate(BaseModel):
    title: Optional[str]
    category_type: Optional[int]
    color: Optional[str]
    active: Optional[bool]


class CategoryInDB(CategoryBase):
    id: int
    owner_id: int
    active: bool
    class Config:
        from_attributes: True
