from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String
from Controller.Database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    category = Column(String, index=True)
    cost = Column(Float, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
