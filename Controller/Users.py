from pydantic import BaseModel, EmailStr
from typing import Optional
from Models.user import User
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Inicializar el contexto de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    Language: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes: True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
