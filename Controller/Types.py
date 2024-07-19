from pydantic import BaseModel


class TypeBase(BaseModel):
    typeName: str


class TypeCreate(TypeBase):
    owner_id: int


class TypeUpdate(BaseModel):
    typeName: str


class TypeInDB(TypeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode: True
