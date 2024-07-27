from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.type import Categorytype
from Models.category import Category
from Models.user import User
from Routes.ManageJWT import get_current_user
from Controller.Categories import CategoryCreate, CategoryUpdate, CategoryInDB
from Controller.Database import get_db

router = APIRouter()


@router.post("/categories/create_category", response_model=CategoryInDB)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_categories = Category(title=category.title,
                            category_type=category.category_type,
                            owner_id=category.owner_id,
                            active = True,
                             color=category.color
                            )
    
    if int(current_user.id) != int(category.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to create this category")
        
    db.add(db_categories)
    db.commit()
    db.refresh(db_categories)
    return db_categories


@router.get("/categories/get_categories/{owner_id}", response_model=List[CategoryInDB])
async def get_categories(owner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if int(current_user.id) != int(owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to get categories")
    
    return db.query(Category).filter(Category.owner_id == owner_id).all()

    

@router.put("/categories/update_category/{category_id}", response_model=CategoryInDB)
async def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_categories = db.query(Category).filter(
        Category.id == category_id).first()
    if not db_categories:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if int(current_user.id) != int(db_categories.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to update this category")

    # Verificar si se proporcionó un nuevo category_type y si es válido
    if category.category_type:
        db_category_type = db.query(Categorytype).filter(
            Categorytype.id == category.category_type).first()
        if not db_category_type:
            raise HTTPException(
                status_code=400, detail="Category type does not exist")

    for key, value in category.dict(exclude_unset=True).items():
        print(key, value)
        setattr(db_categories, key, value)

    db.commit()
    db.refresh(db_categories)
    return db_categories



@router.put("/categories/delete_category/{category_id}", response_model=CategoryInDB)
async def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_categories = db.query(Category).filter(
        Category.id == category_id).first()
    if not db_categories:
        raise HTTPException(status_code=404, detail="Item not found")

    if int(current_user.id) != int(Category.owner_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this category")
    
    setattr(db_categories, 'active', False)
    db.commit()
    db.refresh(db_categories)
    return db_categories
