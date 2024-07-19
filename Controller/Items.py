# Controller/Items.py
from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    title: str
    description: str
    category: str
    cost: float


class ItemCreate(ItemBase):
    owner_id: int


class ItemUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]
    cost: Optional[float]


class ItemInDB(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode: True
