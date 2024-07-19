from sqlalchemy import Column, ForeignKey, Integer, String
from Controller.Database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    category_type = Column(Integer, ForeignKey(
        "category_types.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
