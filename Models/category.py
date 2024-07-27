from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from Controller.Database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category_type = Column(Integer, ForeignKey(
        "category_types.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    color = Column(String, index=True)
    active = Column(Boolean, index=True)
