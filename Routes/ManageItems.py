from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.item import Item
from Models.user import User
from Routes.ManageJWT import get_current_user
from Controller.Items import ItemCreate, ItemUpdate, ItemInDB
from Controller.Database import get_db

router = APIRouter()


@router.post("/items/create_item", response_model=ItemInDB)
async def create_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    if int(current_user.id) != int(item.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to create this item")
    
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.get("/items/get_items/{owner_id}", response_model=List[ItemInDB])
async def get_items(owner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if int(current_user.id) != int(owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to get items")
        
    return db.query(Item).filter(Item.owner_id == owner_id).all()


@router.put("/items/update_item/{item_id}", response_model=ItemInDB)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if int(current_user.id) != int(db_item.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to update this item")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/delete_item/{item_id}", response_model=ItemInDB)
async def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if int(current_user.id) != int(db_item.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to update this item")
    
    db.delete(db_item)
    db.commit()
    return db_item
