from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.type import Categorytype
from Controller.Types import TypeCreate, TypeUpdate, TypeInDB
from Controller.Database import get_db

router = APIRouter()


@router.post("/types/create_type", response_model=TypeInDB)
async def create_types(categorytype: TypeCreate, db: Session = Depends(get_db)):
    db_types = Categorytype(typeName=categorytype.typeName,
                            owner_id=categorytype.owner_id)
    db.add(db_types)
    db.commit()
    db.refresh(db_types)
    return db_types


@router.get("/types/get_types/{owner_id}", response_model=List[TypeInDB])
async def get_types(owner_id: int, db: Session = Depends(get_db)):
    return db.query(Categorytype).filter(Categorytype.owner_id == owner_id).all()


@router.put("/types/update_type/{categorytype_id}", response_model=TypeInDB)
async def update_type(categorytype_id: int, categorytype: TypeUpdate, db: Session = Depends(get_db)):
    db_type = db.query(Categorytype).filter(
        Categorytype.id == categorytype_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in categorytype.dict(exclude_unset=True).items():
        setattr(db_type, key, value)

    db.commit()
    db.refresh(db_type)
    return db_type


@router.delete("/types/delete_type/{categorytype_id}", response_model=TypeInDB)
async def delete_type(categorytype_id: int, db: Session = Depends(get_db)):
    db_type = db.query(Categorytype).filter(
        Categorytype.id == categorytype_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_type)
    db.commit()
    return db_type
