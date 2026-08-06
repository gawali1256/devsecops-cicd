from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema for login requests."""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
