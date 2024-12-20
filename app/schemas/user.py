# schemas/user.py

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="password123")
    confirm_password: str = Field(..., example="password123")

    @field_validator("confirm_password")
    def passwords_match(cls, confirm_password, values, **kwargs):
        password = values.get("password")
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        return confirm_password


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
