from pydantic import BaseModel
from typing import Optional


class TypeBase(BaseModel):
    typeName: str
    active: bool
    color: str
    is_negative: bool

class TypeCreate(BaseModel):
    typeName: str
    owner_id: int
    active: bool
    color: str
    is_negative: bool

class TypeUpdate(BaseModel):
    typeName: Optional[str]
    color: Optional[str]
    active: Optional[bool]
    

class TypeInDB(TypeBase):
    id: int
    owner_id: int

    class Config:
        from_attributes: True
