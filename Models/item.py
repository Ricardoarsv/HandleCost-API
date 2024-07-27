from sqlalchemy import Column, ForeignKey, DateTime, Integer, Float, String
from sqlalchemy.orm import relationship
from Controller.Database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    category = Column(Integer, index=True)
    cost = Column(Float, index=True)
    createDate = Column(DateTime, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))