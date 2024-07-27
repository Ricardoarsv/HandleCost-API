# Controller/Items.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ItemBase(BaseModel):
    title: str
    description: str
    category: int
    cost: float
    createDate: date


class ItemCreate(ItemBase):
    owner_id: int


class ItemUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    category: Optional[int]
    cost: Optional[float]


class ItemInDB(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes: True
