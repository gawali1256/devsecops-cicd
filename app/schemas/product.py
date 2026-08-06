from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """Schema for creating a product."""

    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=1)


class ProductRead(ProductCreate):
    """Schema for reading a product."""

    id: int


class ProductUpdate(BaseModel):
    """Schema for updating a product."""

    name: str | None = None
    price: float | None = None
    stock: int | None = None
    category: str | None = None
