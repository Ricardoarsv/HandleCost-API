from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.type import Categorytype
from Models.user import User
from Routes.ManageJWT import get_current_user
from Controller.Types import TypeCreate, TypeUpdate, TypeInDB
from Controller.Database import get_db

router = APIRouter()


@router.post("/types/create_type", response_model=TypeInDB)
async def create_types(categorytype: TypeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_types = Categorytype(
        typeName=categorytype.typeName,
        owner_id=categorytype.owner_id,
        active=categorytype.active,
        is_negative=categorytype.is_negative,
        color=categorytype.color
    )
    
    if int(current_user.id) != int(categorytype.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to create this type")
    
    db.add(db_types)
    db.commit()
    db.refresh(db_types)
    return db_types


@router.get("/types/get_types/{owner_id}", response_model=List[TypeInDB])
async def get_types(owner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if int(current_user.id) != int(owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to get types")
    return db.query(Categorytype).filter(Categorytype.owner_id == owner_id).all()


@router.put("/types/update_type/{categorytype_id}", response_model=TypeInDB)
async def update_type(categorytype_id: int, categorytype: TypeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_type = db.query(Categorytype).filter(
        Categorytype.id == categorytype_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Item not found")

    if int(current_user.id) != int(db_type.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this user's statistics")
    
    for key, value in categorytype.dict(exclude_unset=True).items():
        setattr(db_type, key, value)

    db.commit()
    db.refresh(db_type)
    return db_type


@router.put("/types/delete_type/{categorytype_id}", response_model=TypeInDB)
async def delete_type(categorytype_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_type = db.query(Categorytype).filter(
        Categorytype.id == categorytype_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if int(current_user.id) != int(Categorytype.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this type")

    setattr(db_type, 'active', False)
    db.commit()
    db.refresh(db_type)
    return db_type
