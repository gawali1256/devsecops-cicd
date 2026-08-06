from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a user."""

    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=4)


class UserRead(BaseModel):
    """Schema for reading a user."""

    id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
