from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from Controller.Database import Base


class Categorytype(Base):
    __tablename__ = "category_types"

    id = Column(Integer, primary_key=True, index=True)
    typeName = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    active = Column(Boolean, index=True)
    color = Column(String, index=True)
    is_negative = Column(Boolean, index=True)
