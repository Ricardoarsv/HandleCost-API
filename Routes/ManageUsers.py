from fastapi import APIRouter
from Models.user import User
from Controller.Users import UserBase
from Controller.Database import db_dependency
router = APIRouter()


@router.post("/users/create_user")
async def create_user(user: UserBase, db: db_dependency):
    db_user = User(username=user.username, email=user.email,
                   is_active=user.is_active)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

@router.get("/users/get_users")
async def get_users(db: db_dependency):
    return db.query(User).all()