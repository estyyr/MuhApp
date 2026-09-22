from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(String(10), nullable=False)
    note = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)