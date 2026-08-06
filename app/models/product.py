from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Product(Base):
    """Product ORM model."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)
